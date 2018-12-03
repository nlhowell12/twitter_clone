from django.db import models
from django.contrib.auth.models import User


class TwitterUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    handle = models.CharField(max_length=25)
    following = models.ManyToManyField('self', symmetrical=False)

    def __str__(self):
        return self.username


class Tweet(models.Model):
    user = models.ForeignKey(TwitterUser, on_delete=models.CASCADE)
    body = models.TextField(max_length=140)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.body


class Notification(models.Model):
    user = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    body = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body
