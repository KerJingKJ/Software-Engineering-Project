from .models import Student

def user_notifications(request):
    if request.user.is_authenticated:
        try:
            # Get the student profile
            student = request.user.student
            # Get unread notifications
            notifications = student.notifications.all()
            unread_count = notifications.filter(is_read=False).count()
            return {
                'notifications': notifications,
                'unread_count': unread_count
            }
        except Student.DoesNotExist:
            return {}
    return {}