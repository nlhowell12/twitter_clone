# Generated by Django 2.1.4 on 2018-12-05 19:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_clone', '0004_notification_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='body',
        ),
    ]
