# profiles/models.py
from django.db import models
from django.contrib.auth.models import User
import random

def get_default_profile_picture():
    # Choose a random default profile picture from 1 to 6
    pic_number = random.randint(1, 6)
    return f"profile_pics/default_{pic_number}.jpg"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default=get_default_profile_picture)

    def __str__(self):
        return f"{self.user.username}'s Profile"
