from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Vote, Option


def _invalidate_poll_cache(poll_id):
    if not poll_id:
        return
    key = f"poll_results:{poll_id}"
    cache.delete(key)


@receiver(post_save, sender=Vote)
def vote_saved(sender, instance, created, **kwargs):
    # invalidate cache when a vote is created or updated
    _invalidate_poll_cache(instance.poll_id)


@receiver(post_delete, sender=Vote)
def vote_deleted(sender, instance, **kwargs):
    _invalidate_poll_cache(instance.poll_id)


@receiver(post_save, sender=Option)
def option_saved(sender, instance, created, **kwargs):
    # if options change, invalidate poll results
    _invalidate_poll_cache(instance.poll_id)
