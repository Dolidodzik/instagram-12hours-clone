# Generated by Django 3.0.6 on 2020-05-05 08:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20200505_0850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='followedCount',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(99999999), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='followersCount',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(99999999), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='post',
            name='likesCount',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(99999999), django.core.validators.MinValueValidator(0)]),
        ),
    ]
