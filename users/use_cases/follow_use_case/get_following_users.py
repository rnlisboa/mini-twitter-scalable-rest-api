from users.services import UserService

from users.use_cases.user_use_case.get_user_by_id import GetUserByIdUseCase


class GetFollowingUserUseCase:
    def __init__(self, user_service=None):
        self.user_service = user_service or UserService()

    def execute(self, user_id: str):
        list_user_by_id_use_case = GetUserByIdUseCase()
        
        list_user_by_id_use_case.execute(user_id=user_id)

        return self.user_service.get_following_user(user_id)
    
