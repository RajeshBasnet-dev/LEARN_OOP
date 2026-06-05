"""Signals for submission-derived profile counters."""
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.users.models import UserProfile

from .models import Submission


@receiver(post_save, sender=Submission)
def update_total_submissions(sender, instance, created, **kwargs):
    """Keep UserProfile.total_submissions in sync when submissions are created."""
    if created:
        UserProfile.objects.filter(pk=instance.user_id).update(
            total_submissions=F("total_submissions") + 1
        )
