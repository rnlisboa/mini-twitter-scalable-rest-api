from django.db.models import F, Case, When, IntegerField
from config.settings  import get_redis_client
from django.db        import transaction

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
        
        return post

    def unlike_post(self, user: User, post: PostModel):
        with transaction.atomic():
            existing_like = LikeModel.objects.filter(user=user, post=post).first()
            if existing_like:
                existing_like.delete()
                PostModel.objects.filter(id=post.id).update(
                    like_count=Case(
                        When(like_count__gt=0, then=F('like_count') - 1),
                        default=0,
                        output_field=IntegerField(),
                    )
                )

        
    @handle_not_found("Post não encontrado.")
    def get_post(self, post_id: int):
        post = PostModel.objects.get(id=post_id)
        return post
    
    def get_like_count(self, post_id: int):
        redis_client = get_redis_client()
        count = redis_client.get(f"post:{post_id}:like_count")
        if count is not None:
            return int(count)

        post = PostModel.objects.get(id=post_id)
        redis_client.set(f"post:{post_id}:like_count", post.like_count)
        return post.like_count