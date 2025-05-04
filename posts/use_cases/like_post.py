from config.settings import get_redis_client

from posts.models import PostModel
from posts.services.services import PostService
from django.contrib.auth.models import User

from posts.tasks.like_tasks import like_post_task

class LikePostUseCase:
    def __init__(self, post_service=None):
        self.post_service = post_service or PostService()

    def execute(self, user: User, post: PostModel):
        redis_client = get_redis_client()
        like_post_task.delay(user.id, post.id)
        like_count = redis_client.get(f"post:{post.id}:like_count")

        return int(like_count) if like_count else self.post_service.get_like_count(post.id)

    
