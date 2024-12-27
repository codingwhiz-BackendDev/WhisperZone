# Generated by Django 5.0 on 2024-12-13 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0003_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='anonymousmessage',
            name='time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='anonymousmessage',
            name='OwnerUsername',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='anonymousmessage',
            name='message',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
