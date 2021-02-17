from django.db import models


class SkillLevelModel(models.Model):
    level = models.CharField(max_length=10, null=False)

    def natural_key(self):
        return self.level

    def __str__(self):
        return self.level


class SkillTypeModel(models.Model):
    name = models.CharField(max_length=50, null=False)
    color = models.CharField(max_length=50, null=False)

    def natural_key(self):
        return (self.name, self.color)

    def __str__(self):
        return "{} ({})".format(self.name, self.color)


class SkillModel(models.Model):
    owner = models.ForeignKey("CharacterModel", on_delete=models.CASCADE, null=False)
    img = models.ImageField(upload_to="assets/skills", null=True, blank=True)
    name = models.CharField(max_length=100, null=False)
    desc = models.TextField(null=False)
    stype = models.ForeignKey(
        "SkillTypeModel",
        on_delete=models.CASCADE,
        null=False,
    )
    range = models.IntegerField(null=False)
    targets = models.CharField(max_length=20, null=False)
    cd = models.IntegerField(null=False)
    level = models.ForeignKey("SkillLevelModel", on_delete=models.CASCADE, null=False)
    deprecated = models.BooleanField(default=False)

    class Meta:
        unique_together = (
            "name",
            "level",
        )

    def __str__(self):
        return "{} ({} (Level {}))".format(self.name, self.owner.name, self.level)


class CharacterModel(models.Model):
    rarity = models.CharField(
        choices=[(str(i), str(i)) for i in range(1, 6)], max_length=2, null=False
    )
    name = models.CharField(max_length=50, null=False, unique=True)
    slug = models.SlugField(max_length=50, null=False, unique=True)
    img = models.ImageField(upload_to="assets/characters", null=False)

    def __str__(self):
        return self.name