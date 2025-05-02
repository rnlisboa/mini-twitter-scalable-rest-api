from django.contrib.auth.models import User
from django.db.models           import Q
from posts.models               import LikeModel, PostModel
from utils.decorators.object_utils import handle_not_found


class PostService:
    def register_post(self, owner: User, text: str, status: str, image: str) -> PostModel:
        post = PostModel(
                owner=owner,
                text=text,
                status=status,
                image=image
            )   
        post.save()
        return post
    
    def get_following_post(self, user_id: int, following: list) -> list:
        following_ids = following.filter(user=user_id).values_list('following', flat=True)
        posts = PostModel.objects.filter(Q(owner__in=following_ids)).exclude(owner=user_id).order_by('-created_at')
        
        return posts

    def like_post(self, user: User, post: PostModel):
        existing_like = LikeModel.objects.filter(user=user, post=post).first()

        if existing_like:
            raise ValueError("Você já curtiu este post.")
        
        like = LikeModel(user=user, post=post)
        like.save()
        
        post.like_count += 1
        post.save()
        
        return like
    
    def unlike_post(self, user: User, post: PostModel):
       existing_like = LikeModel.objects.filter(user=user, post=post).first()
       existing_like.delete()
       post.like_count -= 1
        
    @handle_not_found("Post não encontrado.")
    def get_post(self, post_id: int):
        post = PostModel.objects.get(id=post_id)
        return post