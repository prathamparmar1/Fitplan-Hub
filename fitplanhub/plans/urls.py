from django.urls import path
from .views import (
    TrainerPlanView,
    TrainerPlanDetailView,
    PublicPlanListView,
    PlanDetailView,
    UserFeedView,
)

urlpatterns = [
    path('feed/', UserFeedView.as_view()),
    path('trainer/', TrainerPlanView.as_view()),
    path('trainer/<int:plan_id>/', TrainerPlanDetailView.as_view()),
    path('<int:plan_id>/', PlanDetailView.as_view()),
    path('', PublicPlanListView.as_view()),
]
