# Generated by Django 5.0 on 2024-12-24 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0005_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_user',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
