# Generated by Django 5.1 on 2024-09-10 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0013_post_pinned'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Notification',
        ),
    ]
