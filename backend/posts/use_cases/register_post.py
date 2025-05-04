
from posts.services.services import PostService


class RegisterPostUseCase:
    def __init__(self, post_service=None):
        self.post_service = post_service or PostService()

    def execute(self, owner: str, text: str, status: str, image: str):
        return self.post_service.register_post(owner=owner, text=text, status=status, image=image)
    
