from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Group, Follow, User
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

    def get_queryset(self):
        queryset = Post.objects.all()

        group = self.request.query_params.get('group', None)

        if group is not None:
            group = get_object_or_404(Group, id=group)
            queryset = queryset.filter(group=group)
        return queryset

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

    def create(self, request):
        serializer = FollowSerializer(data=request.data)
        if serializer.is_valid():
            following = User.objects.get(
                username=serializer.validated_data['following']['username'])
            user = self.request.user
            if Follow.objects.filter(user=user, following=following):
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
