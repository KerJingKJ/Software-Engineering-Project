from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Application, Notification


@receiver(pre_save, sender=Application)
def application_status_changed(sender, instance, **kwargs):
    if not instance.pk:
        return  # new application, no "change"

    previous = Application.objects.get(pk=instance.pk)

    # Reviewer status change
    if previous.reviewer_status != instance.reviewer_status:
        Notification.objects.create(
            student=instance.student,
            type="Application",
            message=(
                f"Your application for {instance.scholarship.name} "
                f"was {instance.reviewer_status.lower()} by the reviewer."
            ),
            display_at=timezone.now(),
        )

    # Committee status change
    if previous.committee_status != instance.committee_status:
        Notification.objects.create(
            student=instance.student,
            type="Application",
            message=(
                f"Your application for {instance.scholarship.name} "
                f"was {instance.committee_status.lower()} by the committee."
            ),
            display_at=timezone.now(),
        )
