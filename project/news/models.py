from django.conf import settings
from django.db import models
from django.utils import timezone

from django_quill.fields import QuillField


class NewsModel(models.Model):
    title = models.CharField(max_length=250, null=False)
    slug = models.SlugField(max_length=250, null=False)
    content = QuillField(null=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
        default=settings.AUTH_USER_MODEL,
    )
    creation_date = models.DateField(null=False, default=timezone.now)