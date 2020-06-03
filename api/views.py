from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Group, Follow
from .permissions import IsOwnerOrReadOnly, IsUserOrReadOnly
from .serializers import (
    PostSerializer,
    CommentSerializer,
    GroupSerializer,
    FollowSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['group', ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_post(self):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        return post

    def get_queryset(self):
        queryset = Comment.objects.filter(post=self.get_post()).all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsOwnerOrReadOnly]


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsUserOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=following__username', '=user__username']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
