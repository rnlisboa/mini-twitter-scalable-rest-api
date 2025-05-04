from users.services.services import UserService

class GetUserByIdUseCase:
    def __init__(self, user_service=None):
        self.user_service = user_service or UserService()

    def execute(self, user_id: int):
        return self.user_service.get_user_by_id(user_id)
