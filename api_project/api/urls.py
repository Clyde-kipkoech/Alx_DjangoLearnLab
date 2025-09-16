from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet
from rest_framework.authtoken.views import obtain_auth_token

# Router automatically generates all CRUD routes for BookViewSet
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Route for the BookList view (ListAPIView)
    path('books/', BookList.as_view(), name='book-list'),
    
     # Token authentication endpoint
      # Token authentication endpoint:
    # POST { "username": "user", "password": "pass" }
    # -> returns { "token": "abc123..." }
    path('token/', obtain_auth_token, name='api_token_auth'),


      # All router-based CRUD endpoints for BookViewSet
    path('', include(router.urls)),
]
