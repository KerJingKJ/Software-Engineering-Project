from .models import Student
from django.utils import timezone

def user_notifications(request):
    if request.user.is_authenticated:
        try:
            # Get the student profile
            student = request.user.student
            # Get unread notifications
            notifications = (student.notifications.filter(display_at__lte=timezone.now()))
            unread_count = notifications.filter(is_read=False).count()
            return {
                'notifications': notifications,
                'unread_count': unread_count
            }
        except Student.DoesNotExist:
            return {}
    return {}