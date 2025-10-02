from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Auth routes
    path("login/", auth_views.LoginView.as_view(template_name="blog/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="blog/logout.html"), name="logout"),
    path("register/", views.register_view, name="register"),
    path("profile/", views.profile_view, name="profile"),

    # Blog Post CRUD routes
    path("", views.PostListView.as_view(), name="post_list"),  
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),  
    path("post/new/", views.PostCreateView.as_view(), name="post_create"),  
    path("post/<int:pk>/update/", views.PostUpdateView.as_view(), name="post_update"),  
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post_delete"),  
    
    
   # Comment CRUD
    path("post/<int:pk>/comments/new/", views.CommentCreateView.as_view(), name="comment-create"),
    path("comment/<int:pk>/update/", views.CommentUpdateView.as_view(), name="comment-update"),
    path("comment/<int:pk>/delete/", views.CommentDeleteView.as_view(), name="comment-delete"),
    
    # tag & search
path('tags/<str:tag_name>/', views.posts_by_tag, name='posts-by-tag'),
path('search/', views.search_view, name='post-search'),
]
