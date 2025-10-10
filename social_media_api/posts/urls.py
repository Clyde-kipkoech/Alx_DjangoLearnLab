from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet

# Initialize the router
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

# Include router-generated routes
urlpatterns = [
    path('', include(router.urls)),
    path('feed/', FeedView.as_view(), name='user-feed')
]
