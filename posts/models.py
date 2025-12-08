from django.db import models
from django.conf import settings.AUTH_USER_MODEL as User

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()


class Post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='posts', default='1')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
