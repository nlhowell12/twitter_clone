# Generated by Django 2.1.4 on 2018-12-06 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_clone', '0005_remove_notification_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='viewed',
            field=models.BooleanField(default=False),
        ),
    ]
