
from django.core.management.base import BaseCommand
from nsfp_core.models import TeamNeeds

class Command(BaseCommand):
    help = 'Edit a team needs post content'

    def add_arguments(self, parser):
        parser.add_argument('post_id', type=int, help='ID of the needs post')
        parser.add_argument('content', type=str, help='New content for the post')

    def handle(self, *args, **options):
        post = TeamNeeds.objects.get(pk=options['post_id'])
        old_content = post.content
        post.content = options['content']
        post.save()
        
        self.stdout.write(self.style.SUCCESS(
            f"Successfully updated post {post.id}\n"
            f"Old content: {old_content}\n"
            f"New content: {post.content}"
        ))

