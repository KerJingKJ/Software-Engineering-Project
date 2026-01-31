from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Application, Notification
from committee.models import Interview


@receiver(pre_save, sender=Application)
def application_status_changed(sender, instance, **kwargs):
    if not instance.pk:
        return

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


@receiver(post_save, sender=Interview)
def interview_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            student=instance.application.student,
            type="Interview",
            message=(
                f"An interview for {instance.application.scholarship.name} "
                f"has been scheduled on {instance.date} at {instance.interview_time}."
            ),
            display_at=timezone.now(),
        )
    else:
        # Interview updated
        previous = Interview.objects.get(pk=instance.pk)
        fields_changed = []

        if previous.date != instance.date:
            fields_changed.append("date")
        if previous.interview_time != instance.interview_time:
            fields_changed.append("time")
        if previous.location != instance.location:
            fields_changed.append("location")
        if previous.committee != instance.committee:
            fields_changed.append("committee")

        if fields_changed:
            Notification.objects.create(
                student=instance.application.student,
                type="Interview",
                message=(
                    f"Your interview for {instance.application.scholarship.name} "
                    f"has been updated ({', '.join(fields_changed)} changed). "
                    f"New schedule: {instance.date} at {instance.interview_time}."
                ),
                display_at=timezone.now(),
            )