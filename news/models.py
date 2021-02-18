from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from django_quill.fields import QuillField


class NewsModel(models.Model):
    title = models.CharField(max_length=250, null=False)
    slug = models.SlugField(max_length=250, null=False, unique=True)
    content = QuillField(null=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
        default=1,
    )
    creation_date = models.DateField(null=False, default=timezone.now)

    def __str__(self):
        return "{} ({})".format(self.title, self.author)
