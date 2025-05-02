
from posts.models import PostModel
from posts.services.services import PostService
from django.contrib.auth.models import User


class LikePostUseCase:
    def __init__(self, post_service=None):
        self.post_service = post_service or PostService()

    def execute(self, user: User, post: PostModel):
        return self.post_service.like_post(user=user, post=post)
    
