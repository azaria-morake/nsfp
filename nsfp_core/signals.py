import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Team, TeamPhoto, StaffMember

# DELETE FILE FROM STORAGE WHEN TeamPhoto IS DELETED
@receiver(post_delete, sender=TeamPhoto)
def delete_team_photo_file(sender, instance, **kwargs):
    if instance.image and instance.image.path and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)

# DELETE FILE FROM STORAGE WHEN Team.profile_picture IS UPDATED OR DELETED
@receiver(pre_save, sender=Team)
def delete_old_profile_picture_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return  # New instance — no need to delete

    try:
        old_instance = Team.objects.get(pk=instance.pk)
    except Team.DoesNotExist:
        return

    old_file = old_instance.profile_picture
    new_file = instance.profile_picture

    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

@receiver(post_delete, sender=Team)
def delete_profile_picture_on_team_delete(sender, instance, **kwargs):
    if instance.profile_picture and os.path.isfile(instance.profile_picture.path):
        os.remove(instance.profile_picture.path)


# Delete old profile picture when a new one is uploaded
@receiver(pre_save, sender=StaffMember)
def delete_old_staff_picture_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return  # New object, nothing to delete

    try:
        old_instance = StaffMember.objects.get(pk=instance.pk)
    except StaffMember.DoesNotExist:
        return

    old_file = old_instance.profile_picture
    new_file = instance.profile_picture

    if old_file and old_file != new_file and os.path.isfile(old_file.path):
        os.remove(old_file.path)

# Delete profile picture when staff member is deleted
@receiver(post_delete, sender=StaffMember)
def delete_staff_picture_on_delete(sender, instance, **kwargs):
    file = instance.profile_picture
    if file and os.path.isfile(file.path):
        os.remove(file.path)