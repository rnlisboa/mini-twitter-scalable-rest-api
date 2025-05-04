from django.urls import path
from rest_framework import routers

from posts.views.like_view import LikeViewSet
from posts.views.post_view import PostViewSet
from .views import *


router = routers.DefaultRouter()
router.register('', PostViewSet)
router.register('like', LikeViewSet)

urlpatterns = router.urls