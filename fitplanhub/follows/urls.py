from django.urls import path
from .views import (
    FollowTrainerView,
    UnfollowTrainerView,
    FollowedTrainersView
)

urlpatterns = [
    path('<int:trainer_id>/follow/', FollowTrainerView.as_view()),
    path('<int:trainer_id>/unfollow/', UnfollowTrainerView.as_view()),
    path('my/', FollowedTrainersView.as_view()),
]
