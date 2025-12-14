from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import TrainerFollow
from accounts.models import User

class FollowTrainerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, trainer_id):
        if request.user.role != 'user':
            return Response(
                {"detail": "Only users can follow trainers"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            trainer = User.objects.get(id=trainer_id, role='trainer')
        except User.DoesNotExist:
            return Response({"detail": "Trainer not found"}, status=404)

        follow, created = TrainerFollow.objects.get_or_create(
            user=request.user,
            trainer=trainer
        )

        if not created:
            return Response({"message": "Already following"})

        return Response({"message": "Trainer followed"})


class UnfollowTrainerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, trainer_id):
        try:
            follow = TrainerFollow.objects.get(
                user=request.user,
                trainer_id=trainer_id
            )
        except TrainerFollow.DoesNotExist:
            return Response({"detail": "Not following"}, status=400)

        follow.delete()
        return Response({"message": "Unfollowed"})

class FollowedTrainersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        follows = TrainerFollow.objects.select_related('trainer')\
            .filter(user=request.user)

        data = []
        for item in follows:
            data.append({
                "id": item.trainer.id,
                "name": item.trainer.name,
                "email": item.trainer.email
            })

        return Response(data)
