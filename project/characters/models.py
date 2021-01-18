from django.db import models


class SkillTypeModel(models.Model):
    skill_type_name = models.CharField(max_length=50, null=False)
    skill_type_color = models.CharField(max_length=50, null=False)

    def __str__(self):
        return "{} ({})".format(self.skill_type_name, self.skill_type_color)


class SkillModel(models.Model):
    skill_img = models.ImageField(upload_to="assets/skills", null=False)
    skill_name = models.CharField(max_length=100, null=False, unique=True)
    skill_desc = models.TextField(null=False)
    skill_type = models.ForeignKey(
        "SkillTypeModel", on_delete=models.CASCADE, null=False
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
    char_skill_1 = models.ForeignKey(
        "SkillModel", on_delete=models.CASCADE, null=False, related_name="char_skill_1"
    )
    char_skill_2 = models.ForeignKey(
        "SkillModel", on_delete=models.CASCADE, null=False, related_name="char_skill_2"
    )
    char_skill_3 = models.ForeignKey(
        "SkillModel", on_delete=models.CASCADE, null=False, related_name="char_skill_3"
    )
    char_skill_4 = models.ForeignKey(
        "SkillModel", on_delete=models.CASCADE, null=False, related_name="char_skill_4"
    )
    char_skill_5 = models.ForeignKey(
        "SkillModel", on_delete=models.CASCADE, null=False, related_name="char_skill_5"
    )
    char_skill_6 = models.ForeignKey(
        "SkillModel", on_delete=models.CASCADE, null=False, related_name="char_skill_6"
    )
    char_skill_7 = models.ForeignKey(
        "SkillModel", on_delete=models.CASCADE, null=False, related_name="char_skill_7"
    )
    char_skill_8 = models.ForeignKey(
        "SkillModel", on_delete=models.CASCADE, null=False, related_name="char_skill_8"
    )
    char_skill_9 = models.ForeignKey(
        "SkillModel", on_delete=models.CASCADE, null=False, related_name="char_skill_9"
    )

    def __str__(self):
        return self.char_name