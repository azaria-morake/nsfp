# core/tests/test_authentication.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from knox.models import AuthToken
from nsfp_core.models import Team
import time
from django.utils import timezone
from datetime import timedelta
from django.test import TestCase

class AuthenticationTests(TestCase):
    def test_sample(self):
        self.assertEqual(1+1, 2)

class TokenLifecycleTests(APITestCase):
    def setUp(self):
        self.user = Team.objects.create_user(
            username='test_team',
            team_name='Test Team',
            password='validpass123',
            location='Test City'
        )
        self.token = AuthToken.objects.create(self.user)[1]
        
    # Test 1: Token Expiration
    def test_token_expiration(self):
        # Access protected endpoint with valid token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        response = self.client.get(reverse('team-detail'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Expire the token (simulate waiting past TTL)
        old_token = AuthToken.objects.get(token_key=self.token[:8])
        old_token.expiry = timezone.now() - timedelta(seconds=1)
        old_token.save()
        
        # Attempt request with expired token
        response = self.client.get(reverse('team-detail'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('expired', response.data['detail'].lower())

    # Test 2: Token Rotation
    def test_token_rotation(self):
        # Get new token via refresh
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        response = self.client.post(reverse('token_refresh'))
        new_token = response.data['token']
        
        # Verify old token is invalid
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        response = self.client.get(reverse('team-detail'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Verify new token works
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {new_token}')
        response = self.client.get(reverse('team-detail'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test 3: Refresh Expired Token
    def test_refresh_expired_token(self):
        # Expire the token first
        old_token = AuthToken.objects.get(token_key=self.token[:8])
        old_token.expiry = timezone.now() - timedelta(seconds=1)
        old_token.save()
        
        # Attempt refresh with expired token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        response = self.client.post(reverse('token_refresh'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Test 4: Multiple Refresh Invalidation
    def test_multiple_refresh_invalidation(self):
        # First refresh
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        response1 = self.client.post(reverse('token_refresh'))
        token1 = response1.data['token']
        
        # Second refresh
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token1}')
        response2 = self.client.post(reverse('token_refresh'))
        token2 = response2.data['token']
        
        # Verify all previous tokens are invalid
        for invalid_token in [self.token, token1]:
            self.client.credentials(HTTP_AUTHORIZATION=f'Token {invalid_token}')
            response = self.client.get(reverse('team-detail'))
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Verify latest token works
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token2}')
        response = self.client.get(reverse('team-detail'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)