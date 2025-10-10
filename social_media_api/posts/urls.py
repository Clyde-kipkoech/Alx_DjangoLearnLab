from django.urls import path
from . import views

urlpatterns = [
    # other post routes
    # path('', views.PostListView.as_view(), name='post-list'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),

    # ✅ Add these two lines:
    path('<int:pk>/like/', views.like_post, name='like-post'),
    path('<int:pk>/unlike/', views.unlike_post, name='unlike-post'),
]
