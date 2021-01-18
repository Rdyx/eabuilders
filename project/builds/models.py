from django.db import models
from django.contrib.auth.models import User

from items.models import ItemModel

# Create your models here.
class BuildModel(models.Model):
    # build_creator =
    build_name = models.CharField(max_length=100, null=False)
    build_notes = models.TextField(blank=True, null=True)
    build_item_1 = models.ForeignKey(
        "items.ItemModel", on_delete=models.CASCADE, null=False
    )

    def __str__(self):
        return "ok"
