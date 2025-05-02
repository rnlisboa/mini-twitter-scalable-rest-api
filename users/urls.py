from django.urls import path
from rest_framework import routers

from users.views.follow_view import FollowViewSet
from users.views.user_view import UserViewSet

router = routers.DefaultRouter()
router.register('', UserViewSet)
router.register('follow', FollowViewSet)
urlpatterns = router.urls