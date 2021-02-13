from django.conf import settings
from django.db import models
from django.utils import timezone

from django_quill.fields import QuillField


class BuildModel(models.Model):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
    )
    version = models.IntegerField(null=False)
    creation_date = models.DateField(null=False, default=timezone.now)
    name = models.CharField(max_length=100, null=False)
    slug = models.SlugField(max_length=120, null=False, unique=True)
    notes = QuillField(max_length=500, blank=True, null=True)
    char = models.ForeignKey(
        "characters.CharacterModel", on_delete=models.CASCADE, null=False
    )
    game_mode = models.CharField(
        choices=[(i, i) for i in ["Lab", "Arena"]], max_length=15, null=False
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
        return "{} (v{}) by {}".format(self.name, self.version, self.creator)


class TeamModel(models.Model):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
    )
    creation_date = models.DateField(null=False, default=timezone.now)
    name = models.CharField(max_length=100, null=False, unique=True)
    slug = models.SlugField(max_length=120, null=False, unique=True)
    notes = QuillField(max_length=500, blank=True, null=True)
    game_mode = models.CharField(
        choices=[(i, i) for i in ["Lab", "Arena"]], max_length=15, null=False
    )
    build_1 = models.ForeignKey(
        "BuildModel", on_delete=models.CASCADE, null=False, related_name="build_1"
    )
    build_2 = models.ForeignKey(
        "BuildModel", on_delete=models.CASCADE, null=False, related_name="build_2"
    )
    build_3 = models.ForeignKey(
        "BuildModel", on_delete=models.CASCADE, null=False, related_name="build_3"
    )

    def __str__(self):
        return "{} by {}".format(self.name, self.creator)