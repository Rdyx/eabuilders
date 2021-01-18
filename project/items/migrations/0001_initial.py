# Generated by Django 3.1.5 on 2021-01-18 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ItemsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.IntegerField(unique=True)),
                ('item_tier', models.IntegerField()),
                ('item_img', models.ImageField(upload_to='')),
                ('item_buy_cost', models.IntegerField()),
                ('item_sell_cost', models.IntegerField(null=True)),
                ('item_name', models.CharField(max_length=100, unique=True)),
                ('item_desc', models.CharField(max_length=1000)),
                ('item_hp', models.IntegerField(default=0)),
                ('item_phys_atk', models.IntegerField(default=0)),
                ('item_mag_atk', models.IntegerField(default=0)),
                ('item_phys_def', models.IntegerField(default=0)),
                ('item_mag_def', models.IntegerField(default=0)),
                ('item_acc', models.IntegerField(default=0)),
                ('item_res', models.IntegerField(default=0)),
                ('item_ign_phys', models.IntegerField(default=0)),
                ('item_ign_mag', models.IntegerField(default=0)),
                ('item_speed', models.IntegerField(default=0)),
                ('item_crit_rate', models.IntegerField(default=0)),
                ('item_crit_dmg', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='RacesModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('race_id', models.IntegerField(unique=True)),
                ('race_img', models.ImageField(upload_to='')),
                ('race_name', models.CharField(max_length=150, unique=True)),
                ('race_bonus_1', models.CharField(max_length=1000)),
                ('race_bonus_2', models.CharField(max_length=1000)),
                ('race_bonus_3', models.CharField(max_length=1000)),
            ],
        ),
    ]
