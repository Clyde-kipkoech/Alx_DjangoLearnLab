from django.urls import path
from . import views

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notifications_list'),
    path('<int:notification_id>/read/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('read_all/', views.mark_all_notifications_as_read, name='mark_all_notifications_as_read'),
]
