
from django.core.management.base import BaseCommand
from nsfp_core.models import TeamNeeds

class Command(BaseCommand):
    help = 'Delete a team needs post'

    def add_arguments(self, parser):
        parser.add_argument('post_id', type=int, help='ID of the needs post to delete')

    def handle(self, *args, **options):
        post = TeamNeeds.objects.get(pk=options['post_id'])
        team_name = post.team.team_name
        
        if input(f"Are you sure you want to delete post {post.id} from {team_name}? (yes/no): ").lower() == 'yes':
            post.delete()
            self.stdout.write(self.style.SUCCESS(f"Deleted post {options['post_id']}"))
        else:
            self.stdout.write(self.style.WARNING("Deletion cancelled"))