from django.db import models
from users.models import User
from django_extensions.db.models import TimeStampedModel
# Create your models here.

class Following(TimeStampedModel):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    followed_user = models.ForeignKey(User, related_name='followed_user', on_delete=models.CASCADE)
