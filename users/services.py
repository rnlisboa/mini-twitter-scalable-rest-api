from django.contrib.auth.models import User

from users.models import FollowModel
from utils.object_utils import handle_not_found

class UserService:
    def create_user(self, username: str, email: str, password: str) -> User:
        if User.objects.filter(username=username).exists():
            raise ValueError("Nome de usuário já existe.")
        if User.objects.filter(email=email).exists():
            raise ValueError("Email já existe.")

        user = User(
            username=username,
            email=email,
            is_active=True,
            is_superuser=False
        )
        user.set_password(password)
        user.save()
        return user

    def follow_user(self, user_id: str, follower_id: str) -> User:
        user = self.get_user_by_id(user_id=user_id)
        follower = self.get_user_by_id(user_id=follower_id)
        
        existing_follow = FollowModel.objects.filter(user=user, following=follower).exists()
        if existing_follow:
            raise ValueError("Você já está seguindo o usuário.")
    
        follow = FollowModel(user=user, following=follower)
        follow.save()
        return follow
    
    def unfollow_user(self, user_id: str, follower_id: str) -> None:
        user = self.get_user_by_id(user_id=user_id)
        follower = self.get_user_by_id(user_id=follower_id)
        
        existing_follow = FollowModel.objects.filter(user=user, following=follower)
        if not existing_follow.exists():
            raise ValueError("Você não está seguindo o usuário.")
    
        existing_follow.delete()
    
    def get_following_user(self, user_id) -> list:
        user = self.get_user_by_id(user_id=user_id)
        
        followers = FollowModel.objects.filter(user=user)
        return followers
    
    def list_all_users(self) -> list:

        return User.objects.all()

    @handle_not_found("Usuário não encontrado.")
    def get_user_by_id(self, user_id: str) -> User:
        user = User.objects.get(id=user_id)
        return user
    
    @handle_not_found("Usuário não encontrado.")
    def get_user_by_username(self, username: str) -> User:
        user = User.objects.get(username=username)
        if not user:
            raise ValueError("Usuário não encontrado.")
        
        return user
    
    @handle_not_found("Usuário não encontrado.")
    def get_user_by_email(self, email: str) -> User:
        user = User.objects.get(email=email)
        if not user:
            raise ValueError("Usuário não encontrado.")
        
        return user
