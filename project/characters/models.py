from django.db import models


class SkillTypeManager(models.Manager):
    def get_by_natural_key(self, name, color):
        return self.get(name=name, color=color)


class SkillTypeModel(models.Model):
    name = models.CharField(max_length=50, null=False)
    color = models.CharField(max_length=50, null=False)

    objects = SkillTypeManager()

    class Meta:
        unique_together = ["name", "color"]

    def natural_key(self):
        return (self.name, self.color)

    def __str__(self):
        return "{} ({})".format(self.name, self.color)


class SkillModel(models.Model):
    skill_owner = models.ForeignKey(
        "CharacterModel", on_delete=models.CASCADE, null=False
    )
    skill_img = models.ImageField(upload_to="assets/skills", null=False)
    skill_name = models.CharField(max_length=100, null=False, unique=True)
    skill_desc = models.TextField(null=False)
    skill_type = models.ForeignKey(
        "SkillTypeModel",
        on_delete=models.CASCADE,
        null=False,
        related_name="skill_type",
    )
    skill_range = models.IntegerField(null=False)
    skill_targets = models.CharField(max_length=20, null=False)
    skill_cd = models.IntegerField(null=False)

    def __str__(self):
        return self.skill_name


class CharacterModel(models.Model):
    char_name = models.CharField(max_length=50, null=False, unique=True)
    char_slug = models.SlugField(max_length=50, null=False, unique=True)
    char_img = models.ImageField(upload_to="assets/characters", null=False)

    def __str__(self):
        return self.char_name