from .models import CommitteeNotification

def committee_notif_context(request):
    if request.user.is_authenticated and 'committee.mmu.edu.my' in request.user.email:
        # Get only the last 5 unread/recent alerts for this specific user
        alerts = CommitteeNotification.objects.filter(user=request.user)
        return {
            'comm_alerts': alerts[:5],
            'comm_unread_count': alerts.filter(is_read=False).count()
        }
    return {}