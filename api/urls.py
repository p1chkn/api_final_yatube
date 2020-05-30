from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import PostViewSet, CommentViewSet, GroupViewSet, FollowViewSet

router = DefaultRouter()
router.register('api/v1/posts', PostViewSet)
router.register('api/v1/group', GroupViewSet)
router.register('api/v1/follow', FollowViewSet)
router_comment = DefaultRouter()
router_comment.register('', CommentViewSet)

urlpatterns = [
    path('api/v1/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('', include(router.urls)),
    path('api/v1/posts/<int:post_id>/comments/', include(router_comment.urls)),
]
