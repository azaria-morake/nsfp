// src/pages/AuthPage.jsx
import { useState } from 'react';
import styled from 'styled-components';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

const AuthContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 24px;
  min-height: 100vh;
  background-color: #f5f5f5;
`;

const Logo = styled.div`
  width: 120px;
  height: 120px;
  background-color: #ddd;
  border-radius: 50%;
  margin-bottom: 24px;
`;

const Description = styled.p`
  text-align: center;
  margin-bottom: 32px;
  font-size: 16px;
  color: #333;
  max-width: 300px;
`;

const AuthButton = styled.button`
  width: 100%;
  max-width: 300px;
  padding: 16px;
  margin-bottom: 16px;
  border: none;
  border-radius: 8px;
  background-color: #eee;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
`;

const AuthForm = styled.form`
  width: 100%;
  max-width: 300px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: ${({ $isOpen }) => ($isOpen ? '16px' : '0')};
  max-height: ${({ $isOpen }) => ($isOpen ? '500px' : '0')};
  overflow: hidden;
  transition: all 0.3s ease;
`;

const InputField = styled.input`
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 16px;
`;

const SubmitButton = styled.button`
  padding: 16px;
  background-color: #333;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
`;

export default function AuthPage() {
  const [activeForm, setActiveForm] = useState(null);
  const [loginData, setLoginData] = useState({ username: '', password: '' });
  const [registerData, setRegisterData] = useState({
    username: '',
    team_name: '',
    password: '',
    password2: '',
    location: ''
  });
  const { login, register } = useAuth();
  const navigate = useNavigate();

  const toggleForm = (formType) => {
    setActiveForm(activeForm === formType ? null : formType);
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      await login(loginData.username, loginData.password);
      navigate('/dashboard');
    } catch (error) {
      console.error('Login failed', error);
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    if (registerData.password !== registerData.password2) {
      alert("Passwords don't match!");
      return;
    }
    try {
      await register(registerData);
      navigate('/dashboard');
    } catch (error) {
      console.error('Registration failed', error);
    }
  };

  return (
    <AuthContainer>
      <Logo />
      <Description>
        Connect with your football community. Manage your team, track progress, and compete with others.
      </Description>

      <AuthButton onClick={() => toggleForm('login')}>
        Login
      </AuthButton>

      <AuthForm $isOpen={activeForm === 'login'} onSubmit={handleLogin}>
        <InputField
          type="text"
          placeholder="Username"
          value={loginData.username}
          onChange={(e) => setLoginData({...loginData, username: e.target.value})}
        />
        <InputField
          type="password"
          placeholder="Password"
          value={loginData.password}
          onChange={(e) => setLoginData({...loginData, password: e.target.value})}
        />
        <SubmitButton type="submit">Login</SubmitButton>
      </AuthForm>

      <AuthButton onClick={() => toggleForm('register')}>
        Register
      </AuthButton>

      <AuthForm $isOpen={activeForm === 'register'} onSubmit={handleRegister}>
        <InputField
          type="text"
          placeholder="Username"
          value={registerData.username}
          onChange={(e) => setRegisterData({...registerData, username: e.target.value})}
        />
        <InputField
          type="text"
          placeholder="Team Name"
          value={registerData.team_name}
          onChange={(e) => setRegisterData({...registerData, team_name: e.target.value})}
        />
        <InputField
          type="text"
          placeholder="Location"
          value={registerData.location}
          onChange={(e) => setRegisterData({...registerData, location: e.target.value})}
        />
        <InputField
          type="password"
          placeholder="Password"
          value={registerData.password}
          onChange={(e) => setRegisterData({...registerData, password: e.target.value})}
        />
        <InputField
          type="password"
          placeholder="Confirm Password"
          value={registerData.password2}
          onChange={(e) => setRegisterData({...registerData, password2: e.target.value})}
        />
        <SubmitButton type="submit">Register</SubmitButton>
      </AuthForm>
    </AuthContainer>
  );
}