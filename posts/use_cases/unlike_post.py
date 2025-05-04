
from posts.models import PostModel
from posts.services.services import PostService
from django.contrib.auth.models import User


class UnLikePostUseCase:
    def __init__(self, post_service=None):
        self.post_service = post_service or PostService()

    def execute(self, user: User, post: PostModel):
        self.post_service.unlike_post(user=user, post=post)
    
