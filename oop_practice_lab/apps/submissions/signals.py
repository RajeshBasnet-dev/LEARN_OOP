"""Signals for submission-derived profile counters."""
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Submission


@receiver(post_save, sender=Submission)
def update_total_submissions(sender, instance, created, **kwargs):
    """Keep UserProfile.total_submissions in sync when submissions are created."""
    if created:
        user = instance.user
        user.total_submissions = Submission.objects.filter(user=user).count()
        user.save(update_fields=["total_submissions"])
