from django.db import models


class SkillTypeModel(models.Model):
    name = models.CharField(max_length=50, null=False)
    color = models.CharField(max_length=50, null=False)

    def natural_key(self):
        return (self.name, self.color)

    def __str__(self):
        return "{} ({})".format(self.name, self.color)


class SkillModel(models.Model):
    owner = models.ForeignKey("CharacterModel", on_delete=models.CASCADE, null=False)
    img = models.ImageField(upload_to="assets/skills", null=False)
    name = models.CharField(max_length=100, null=False, unique=True)
    desc = models.TextField(null=False)
    stype = models.ForeignKey(
        "SkillTypeModel",
        on_delete=models.CASCADE,
        null=False,
        related_name="type",
    )
    range = models.IntegerField(null=False)
    targets = models.CharField(max_length=20, null=False)
    cd = models.IntegerField(null=False)

    def __str__(self):
        return self.name


class CharacterModel(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    slug = models.SlugField(max_length=50, null=False, unique=True)
    img = models.ImageField(upload_to="assets/characters", null=False)

    def __str__(self):
        return self.name