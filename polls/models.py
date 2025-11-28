from django.db import models
from django.utils import timezone
from django.conf import settings
import uuid


class Poll(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='polls'
    )
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['-created_at'])]

    def __str__(self):
        return self.title

    def has_expired(self):
        return self.expires_at is not None and timezone.now() >= self.expires_at


class Option(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    poll = models.ForeignKey(Poll, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('poll', 'text'),)
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.text} ({self.poll.title})"


class Vote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    poll = models.ForeignKey(Poll, related_name='votes', on_delete=models.CASCADE)
    option = models.ForeignKey(Option, related_name='votes', on_delete=models.CASCADE)
    voter_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('poll', 'voter_id'),)
        indexes = [models.Index(fields=['voter_id', 'poll']), models.Index(fields=['poll'])]

    def __str__(self):
        return f"Vote by {self.voter_id} on {self.poll.title} -> {self.option.text}"
