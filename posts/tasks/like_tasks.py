from __future__ import absolute_import, unicode_literals

from config.settings import get_redis_client
from celery import shared_task
from django.db import transaction
from posts.services.services import PostService
from users.services.services import UserService
@shared_task
def like_post_task(user_id: int, post_id: int):

    post_service = PostService()
    user_service = UserService()
    with transaction.atomic():
        user = user_service.get_user_by_id(user_id=user_id)
        post = post_service.get_post(post_id=post_id)
        
        post_updated = post_service.like_post(user=user, post=post)
        redis_client = get_redis_client()
        redis_client.incr(f"post:{post.id}:like_count")
        return {"post_id": post_updated.id, "like_count": post_updated.like_count}

