from .models import Subscription

def has_active_subscription(user, plan):
    return Subscription.objects.filter(
        user=user,
        plan=plan,
        is_active=True
    ).exists()
