# Generated by Django 5.0 on 2025-02-18 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0017_voterecord'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessagesLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField()),
                ('message', models.CharField(max_length=255)),
            ],
        ),
    ]
