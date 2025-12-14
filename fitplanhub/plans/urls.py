from django.urls import path
from .views import (
    TrainerPlanView,
    TrainerPlanDetailView,
    PublicPlanListView,
    PlanDetailView,
    UserFeedView,
)

urlpatterns = [
    path('', PublicPlanListView.as_view()),
    path('trainer/', TrainerPlanView.as_view()),
    path('trainer/<int:plan_id>/', TrainerPlanDetailView.as_view()),
    path('api/plans/<int:plan_id>/', PlanDetailView.as_view()),
    path('feed/', UserFeedView.as_view()),
]
