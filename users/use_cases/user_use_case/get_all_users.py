from users.services import UserService

class GetAllUsersUseCase:
    def __init__(self, user_service=None):
        self.user_service = user_service or UserService()

    def execute(self):
        self.user_service.list_all_users()