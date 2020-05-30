from rest_framework import serializers
from django.shortcuts import get_object_or_404

from .models import Post, Comment, Group, Follow, User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', required=False)

    class Meta:
        fields = ['id', 'text', 'pub_date', 'author', 'group']
        read_only_fields = ['author']
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', required=False)
    text = serializers.CharField(required=False)

    class Meta:
        fields = ['id', 'text', 'author', 'post', 'created']
        read_only_fields = ['author']
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False)
    description = serializers.CharField(required=False)

    class Meta:
        fields = ['id', 'title', 'slug', 'description']
        model = Group


class FollowSerializer(serializers.ModelSerializer):

    user = serializers.CharField(source='user.username', required=False)
    following = serializers.CharField(source='following.username')

    class Meta:
        fields = ['id', 'user', 'following']
        read_only_fields = ['user']
        model = Follow

    def create(self, validated_data):
        user = get_object_or_404(User, username=validated_data['user'])
        following = get_object_or_404(
            User, username=validated_data['following']['username'])
        follow = Follow(user=user, following=following)
        follow.save()
        return follow
