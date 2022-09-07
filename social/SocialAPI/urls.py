from django.urls import path, include, re_path
from rest_framework import routers

from SocialAPI.views import *

router = routers.DefaultRouter()
router.register(r'posts', PostsModelViewSet)
print(router.urls)
router.register(r'group', GroupModelViewSet)
router.register(r'posts/(?P<post_id>[^/.]+)/comments', CommentModelViewSet)
router.register(r'follow', FollowModelViewSet)


urlpatterns = [
    # Routers
    path('v1/', include(router.urls)),
    # path('v1/posts/<int:post_id>/comments/', include(router.urls)),
    # API Token Authorization
    path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    # API Posts

]