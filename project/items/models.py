from django.db import models


class RaceModel(models.Model):
    race_id = models.IntegerField(unique=True, null=False)
    race_img = models.ImageField(upload_to="assets/race", null=False)
    race_name = models.CharField(max_length=150, unique=True, null=False)
    race_bonus_1 = models.CharField(max_length=1000, null=False)
    race_bonus_2 = models.CharField(max_length=1000, null=False)
    race_bonus_3 = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.race_name


class MaterialModel(models.Model):
    material_id = models.IntegerField(unique=True, null=False)
    material_img = models.ImageField(upload_to="assets/material", null=False)
    material_name = models.CharField(max_length=150, unique=True, null=False)
    material_bonus_1 = models.CharField(max_length=1000, null=False)
    material_bonus_2 = models.CharField(max_length=1000, null=False)
    material_bonus_3 = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.material_name


class ItemModel(models.Model):
    item_id = models.IntegerField(unique=True, null=False)
    item_tier = models.IntegerField(null=False)
    item_img = models.ImageField(upload_to="assets/item", null=False)
    item_buy_cost = models.IntegerField(null=False)
    item_sell_cost = models.IntegerField(blank=True, null=True)
    item_name = models.CharField(max_length=100, unique=True, null=False)
    item_desc = models.CharField(max_length=1000, null=False)
    item_race = models.ForeignKey("RaceModel", on_delete=models.CASCADE, null=False)
    item_material = models.ForeignKey(
        "MaterialModel", on_delete=models.CASCADE, null=False
    )
    item_hp = models.IntegerField(default=0, null=False)
    item_phys_atk = models.IntegerField(default=0, null=False)
    item_mag_atk = models.IntegerField(default=0, null=False)
    item_phys_def = models.IntegerField(default=0, null=False)
    item_mag_def = models.IntegerField(default=0, null=False)
    item_acc = models.IntegerField(default=0, null=False)
    item_res = models.IntegerField(default=0, null=False)
    item_ign_phys = models.IntegerField(default=0, null=False)
    item_ign_mag = models.IntegerField(default=0, null=False)
    item_speed = models.IntegerField(default=0, null=False)
    item_crit_rate = models.IntegerField(default=0, null=False)
    item_crit_dmg = models.IntegerField(default=0, null=False)

    def save(self, *args, **kwargs):
        if not self.item_sell_cost:
            item_sell_cost = int(self.item_buy_cost / 2)  # Game has no .XX values
        super(ItemModel, self).save(*args, **kwargs)

    def __str__(self):
        return "{}. {} ({}, {})".format(
            self.item_id, self.item_name, self.item_race, self.item_material
        )
