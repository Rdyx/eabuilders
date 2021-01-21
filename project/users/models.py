from django.db import models
from django.contrib.auth.models import AbstractUser

from django_quill.fields import QuillField


class User(AbstractUser):
    bio = QuillField(max_length=1500, blank=True, null=True)
    ingame_name = models.CharField(max_length=50, blank=True, null=True)
    discord = models.CharField(max_length=50, null=True, blank=True)
    clan = models.CharField(max_length=15, null=True, blank=True)
