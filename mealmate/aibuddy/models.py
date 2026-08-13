from django.conf import settings
from django.db import models


class ChatLog(models.Model):
    """Keeps a light trail of AI Buddy conversations, useful for improving replies later."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=64, blank=True)
    message = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat @ {self.created_at:%Y-%m-%d %H:%M}"
