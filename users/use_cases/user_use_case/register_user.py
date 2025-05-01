from users.services import UserService

class RegisterUserUseCase:
    def __init__(self, user_service=None):
        self.user_service = user_service or UserService()

    def execute(self, username: str, email: str, password: str):
        return self.user_service.create_user(username, email, password)
