from django.conf import settings
from django.db import models

# from items.models import ItemModel

# Create your models here.
class BuildModel(models.Model):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False
    )
    name = models.CharField(max_length=100, null=False, unique=True)
    slug = models.SlugField(max_length=120, null=False, unique=True)
    notes = models.TextField(blank=True, null=True)
    char = models.ForeignKey(
        "characters.CharacterModel", on_delete=models.CASCADE, null=False
    )
    skill_1 = models.ForeignKey(
        "characters.SkillModel",
        on_delete=models.CASCADE,
        null=False,
        related_name="skill_1",
    )
    skill_2 = models.ForeignKey(
        "characters.SkillModel",
        on_delete=models.CASCADE,
        null=False,
        related_name="skill_2",
    )
    skill_3 = models.ForeignKey(
        "characters.SkillModel",
        on_delete=models.CASCADE,
        null=False,
        related_name="skill_3",
    )
    skill_4 = models.ForeignKey(
        "characters.SkillModel",
        on_delete=models.CASCADE,
        null=False,
        related_name="skill_4",
    )
    skill_5 = models.ForeignKey(
        "characters.SkillModel",
        on_delete=models.CASCADE,
        null=False,
        related_name="skill_5",
    )
    skill_6 = models.ForeignKey(
        "characters.SkillModel",
        on_delete=models.CASCADE,
        null=False,
        related_name="skill_6",
    )
    item_1 = models.ForeignKey(
        "items.ItemModel", on_delete=models.CASCADE, null=False, related_name="item_1"
    )
    item_2 = models.ForeignKey(
        "items.ItemModel", on_delete=models.CASCADE, null=False, related_name="item_2"
    )
    item_3 = models.ForeignKey(
        "items.ItemModel", on_delete=models.CASCADE, null=False, related_name="item_3"
    )
    item_4 = models.ForeignKey(
        "items.ItemModel", on_delete=models.CASCADE, null=False, related_name="item_4"
    )
    item_5 = models.ForeignKey(
        "items.ItemModel", on_delete=models.CASCADE, null=False, related_name="item_5"
    )
    item_6 = models.ForeignKey(
        "items.ItemModel", on_delete=models.CASCADE, null=False, related_name="item_6"
    )
    item_7 = models.ForeignKey(
        "items.ItemModel", on_delete=models.CASCADE, null=False, related_name="item_7"
    )
    item_8 = models.ForeignKey(
        "items.ItemModel", on_delete=models.CASCADE, null=False, related_name="item_8"
    )

    def __str__(self):
        return "{} ({})".format(self.name, self.creator)
