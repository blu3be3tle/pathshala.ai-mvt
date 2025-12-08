from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.


class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(
        User, related_name='profile', on_delete=models.CASCADE)
    bio = models.CharField(max_length=250, blank=True)
