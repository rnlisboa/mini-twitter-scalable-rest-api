from users.services.services import UserService

class GetUserByUsernameUseCase:
    def __init__(self, user_service=None):
        self.user_service = user_service or UserService()

    def execute(self, username: str):
        return self.user_service.get_user_by_username(username)