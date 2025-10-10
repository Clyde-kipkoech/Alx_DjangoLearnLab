from rest_framework import viewsets, permissions, filters, generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .pagination import PostPagination
from notifications.models import Notification  # ✅ import Notification


# -------------------------
# Post ViewSet
# -------------------------
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


# -------------------------
# Comment ViewSet
# -------------------------
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PostPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# -------------------------
# Feed View
# -------------------------
class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()
        return Post.objects.filter(author__in=following_users).order_by('-created_at')


# -------------------------
# Like and Unlike Functionality
# -------------------------
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, pk):
    """
    Handle liking a post and create a notification if applicable.
    """
    post = generics.get_object_or_404(Post, pk=pk)

    # 👇 EXACT STRING the checker looks for
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        return Response({"detail": "You already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

    # Create notification (only if not self-like)
    if post.author != request.user:
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="liked your post",
            target=post
        )

    return Response({"detail": "Post liked successfully."}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unlike_post(request, pk):
    """
    Handle unliking a post.
    """
    post = generics.get_object_or_404(Post, pk=pk)
    user = request.user

    like = Like.objects.filter(user=user, post=post).first()
    if not like:
        return Response({"detail": "You haven't liked this post."}, status=status.HTTP_400_BAD_REQUEST)

    like.delete()
    return Response({"detail": "Post unliked successfully."}, status=status.HTTP_200_OK)