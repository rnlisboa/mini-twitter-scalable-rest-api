from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class FollowModel(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following'
    )
    created_at = models.DateTimeField(auto_now_add=True)