from django.db import models
from django.contrib.auth.models import AbstractUser
from django_extensions.db.models import TimeStampedModel

# Create your models here.


class User(AbstractUser, TimeStampedModel):
    bio = models.CharField(max_length=255, blank=True)
    is_verified = models.BooleanField(default=False)

    def number_of_followers(self):
        return 5

    def number_of_following(self):
        return 5

    def __str__(self):
        return self.username
