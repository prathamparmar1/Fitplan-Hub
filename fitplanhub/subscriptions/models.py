from django.db import models
from django.conf import settings
from plans.models import FitnessPlan

User = settings.AUTH_USER_MODEL

class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    plan = models.ForeignKey(
        FitnessPlan,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    purchased_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'plan')

    def __str__(self):
        return f"{self.user} - {self.plan}"
