from django.db import models
from django.contrib.auth.models import AbstractUser

from django_quill.fields import QuillField


class User(AbstractUser):
    bio = QuillField(max_length=500, blank=True, null=True)
    ingame_name = models.CharField(max_length=50, blank=True, null=True)
    discord = models.CharField(max_length=50, null=True, blank=True)
    guild = models.CharField(max_length=150, null=True, blank=True)
