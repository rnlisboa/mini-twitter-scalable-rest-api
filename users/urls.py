from django.urls import path
from rest_framework import routers

from users.use_cases.follow_use_case.view import FollowViewSet
from users.use_cases.user_use_case.view import UserViewSet

router = routers.DefaultRouter()
router.register('', UserViewSet)
router.register('follow', FollowViewSet)
urlpatterns = router.urls