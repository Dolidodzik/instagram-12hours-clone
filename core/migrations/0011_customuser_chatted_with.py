# Generated by Django 3.0.6 on 2020-05-05 12:09

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='chatted_with',
            field=django_mysql.models.ListCharField(models.CharField(max_length=10), default=[], max_length=200, size=10),
        ),
    ]
