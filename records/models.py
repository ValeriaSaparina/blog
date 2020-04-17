from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20)
    count_posts = models.IntegerField(default=0)
    about = models.CharField(max_length=500, default="")
    my_favorites = models.CharField(max_length=1000, default="")
    count_favorites = models.IntegerField(default=0)


class Post(models.Model):
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=2000)
    author = models.CharField(max_length=20)
    theme = models.CharField(max_length=30)
    pub_date = models.DateTimeField('Date published')
    likes = models.IntegerField(default=0)
