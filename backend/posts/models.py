from django.db import models
from django.contrib.auth.models import User

def upload_image(instance, filename):
    return f'images/posts/user_{instance.owner.id}/{filename}'

class Status(models.IntegerChoices):
    DRAFT = 0, 'Draft'
    PUBLISHED = 1, 'Published'
    ARCHIVED = 2, 'Archived'

class PostModel(models.Model):
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=Status.choices, default=Status.DRAFT)
    image = models.ImageField(
        null=True, blank=True, upload_to=upload_image, default=''
    )
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='User'
    )
    like_count = models.IntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['owner']),
            models.Index(fields=['-created_at']),
        ]

class LikeModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')