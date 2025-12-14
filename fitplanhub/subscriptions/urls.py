from django.urls import path
from .views import SubscribePlanView

urlpatterns = [
    path('<int:plan_id>/', SubscribePlanView.as_view()),
]
