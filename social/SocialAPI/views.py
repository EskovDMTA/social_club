
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, authentication, viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from SocialAPI.sserializers import PostModelSerializer, GroupModelSerializer, FollowModelSerializer, \
    CommentModelSerializer
from posts.models import Posts, Group, Follow, Comment


# class PostsListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Posts.objects.all()
#     serializer_class = PostModelSerializer
#     authentication_classes = (authentication.TokenAuthentication,)


class PostsModelViewSet(viewsets.ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostModelSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['text']


class GroupModelViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupModelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title']


class CommentModelViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentModelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created']

    def get_queryset(self):
        return self.queryset.filter(post=self.kwargs.get('post_id'))

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)


class FollowModelViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowModelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author', 'user']



