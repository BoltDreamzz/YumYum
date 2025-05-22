from django.db import models

# Create your models here.
from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from django.utils.text import slugify
from profiles.models import UserProfile

class Blog(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    slug = models.SlugField(unique=True)
    content = HTMLField()
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)

    # SEO fields
    meta_title = models.CharField(max_length=60, help_text="Max 60 characters", blank=True)
    meta_description = models.CharField(max_length=160, help_text="Max 160 characters", blank=True)
    focus_keyword = models.CharField(max_length=100, help_text="Main keyword for SEO", blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
