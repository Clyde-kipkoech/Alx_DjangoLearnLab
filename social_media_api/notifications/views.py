from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from .models import Notification
from .serializers import NotificationSerializer


# -------------------------
# List Notifications
# -------------------------
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return all notifications for the authenticated user,
        showing unread notifications first.
        """
        user = self.request.user
        return Notification.objects.filter(recipient=user).order_by('is_read', '-timestamp')


# -------------------------
# Mark Notification as Read
# -------------------------
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_notification_as_read(request, notification_id):
    """
    Mark a specific notification as read.
    """
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    return Response({"detail": "Notification marked as read."}, status=status.HTTP_200_OK)


# -------------------------
# Mark All as Read
# -------------------------
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_all_notifications_as_read(request):
    """
    Mark all notifications for the current user as read.
    """
    user = request.user
    Notification.objects.filter(recipient=user, is_read=False).update(is_read=True)
    return Response({"detail": "All notifications marked as read."}, status=status.HTTP_200_OK)
