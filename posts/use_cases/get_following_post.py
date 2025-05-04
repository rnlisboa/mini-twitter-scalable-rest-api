from posts.services.services import PostService
from users.use_cases.follow_use_case.get_following_users import GetFollowingUserUseCase


class GetFollowingPostUseCase:
    def __init__(self, post_service=None):
        self.post_service = post_service or PostService()
    
    def execute(self, user_id: int):
        get_following_use_case = GetFollowingUserUseCase()
        following = get_following_use_case.execute(user_id=user_id)

        return self.post_service.get_following_post(user_id=user_id, following=following)