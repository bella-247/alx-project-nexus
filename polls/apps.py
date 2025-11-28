from django.apps import AppConfig


class PollsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'

    def ready(self):
        # import signals to register cache invalidation handlers
        try:
            from . import signals  # noqa: F401
        except Exception:
            pass
