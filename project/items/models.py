from django.db import models


class RaceModel(models.Model):
    img = models.ImageField(upload_to="assets/race", null=False)
    name = models.CharField(max_length=150, unique=True, null=False)
    slug = models.SlugField(max_length=150, unique=True, null=False)
    bonus_1 = models.CharField(max_length=1000, null=False)
    bonus_2 = models.CharField(max_length=1000, null=False)
    bonus_3 = models.CharField(max_length=1000, blank=True, null=True)

    def natural_key(self):
        return (str(self.img), self.name, self.bonus_1, self.bonus_2, self.bonus_3)

    def __str__(self):
        return self.name


class MaterialModel(models.Model):
    img = models.ImageField(upload_to="assets/material", null=False)
    name = models.CharField(max_length=150, unique=True, null=False)
    slug = models.SlugField(max_length=150, unique=True, null=False)
    bonus_1 = models.CharField(max_length=1000, null=False)
    bonus_2 = models.CharField(max_length=1000, null=False)
    bonus_3 = models.CharField(max_length=1000, blank=True, null=True)

    def natural_key(self):
        return (str(self.img), self.name, self.bonus_1, self.bonus_2, self.bonus_3)

    def __str__(self):
        return self.name


class ItemModel(models.Model):
    tier = models.CharField(choices=[(str(i),str(i)) for i in range(1,6)], max_length=2, null=False)
    img = models.ImageField(upload_to="assets/item", null=False)
    buy_cost = models.IntegerField(null=False)
    sell_cost = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100, unique=True, null=False)
    slug = models.SlugField(max_length=100, unique=True, null=False)
    desc = models.CharField(max_length=1000, null=False)
    race = models.ForeignKey("RaceModel", on_delete=models.CASCADE, null=False)
    material = models.ForeignKey("MaterialModel", on_delete=models.CASCADE, null=False)
    hp = models.IntegerField(default=0, null=False)
    phys_atk = models.IntegerField(default=0, null=False)
    mag_atk = models.IntegerField(default=0, null=False)
    phys_def = models.IntegerField(default=0, null=False)
    mag_def = models.IntegerField(default=0, null=False)
    acc = models.IntegerField(default=0, null=False)
    res = models.IntegerField(default=0, null=False)
    ign_phys = models.IntegerField(default=0, null=False)
    ign_mag = models.IntegerField(default=0, null=False)
    speed = models.IntegerField(default=0, null=False)
    crit_rate = models.IntegerField(default=0, null=False)
    crit_dmg = models.IntegerField(default=0, null=False)

    def save(self, *args, **kwargs):
        if not self.sell_cost:
            sell_cost = int(self.buy_cost / 2)  # Game has no .XX values
        super(ItemModel, self).save(*args, **kwargs)

    def __str__(self):
        return "{}. {} ({}, {})".format(self.id, self.name, self.race, self.material)
