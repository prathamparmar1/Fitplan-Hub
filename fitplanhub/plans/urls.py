from django.urls import path
from .views import (
    TrainerPlanView,
    TrainerPlanDetailView,
    PublicPlanListView
)

urlpatterns = [
    path('', PublicPlanListView.as_view()),
    path('trainer/', TrainerPlanView.as_view()),
    path('trainer/<int:plan_id>/', TrainerPlanDetailView.as_view()),
]
