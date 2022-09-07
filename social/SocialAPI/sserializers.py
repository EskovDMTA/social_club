from rest_framework import serializers

from posts.models import Posts, Group, Comment, Follow


class PostModelSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Posts
        fields = ['id', 'text', 'pub_date', 'author', 'group']


class GroupModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['title', 'slug']


class CommentModelSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'text']


class FollowModelSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Follow
        fields = ['user', 'author']





