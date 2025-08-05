from django.db import models
from django.utils import timezone


class Token(models.Model):
    user_id = models.CharField(max_length=255, unique=True)
    access_token = models.TextField()
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"Token {self.access_token} for user {self.user_id} will expire at {self.expires_at}"

    def is_expired(self):
        return timezone.now() >= self.expires_at

    def update(self, access_token, requested_at):
        self.access_token = access_token
        token_life = timezone.timedelta(seconds=3600)
        expires_at = requested_at + token_life
        self.expires_at = expires_at
        self.save()

    def get_access_token(self):
        if not self.access_token:
            raise ValueError("Access token is not set yet")
        elif self.is_expired():
            raise ValueError("Token is expired")
        return self.access_token
