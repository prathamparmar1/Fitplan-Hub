from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class TrainerFollow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )
    trainer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers'
    )
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'trainer')

    def __str__(self):
        return f"{self.user} follows {self.trainer}"
