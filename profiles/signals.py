# profiles/signals.py
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile
import random

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()


# profiles/signals.py (continued)
from allauth.account.signals import user_logged_in

@receiver(user_logged_in)
def assign_random_profile_pic(sender, request, user, **kwargs):
    profile = user.userprofile
    if not profile.profile_picture or "default" not in profile.profile_picture.name:
        return  # Don't overwrite custom profile pictures

    # Randomly reassign only if they are using the default system
    profile.profile_picture = f"profile_pics/default_{random.randint(1, 6)}.png"
    profile.save()