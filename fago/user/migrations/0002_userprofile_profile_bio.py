# Generated by Django 5.1 on 2024-08-21 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='profile_bio',
            field=models.TextField(null=True),
        ),
    ]
