# posts/views.py
from rest_framework import viewsets, permissions, filters
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .pagination import PostPagination

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PostPagination

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']  # Allows search by title or content
    ordering_fields = ['created_at', 'title']  # Optional: allow ordering by date or title

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PostPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
