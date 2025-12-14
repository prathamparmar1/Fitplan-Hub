from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Subscription
from plans.models import FitnessPlan

class SubscribePlanView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, plan_id):
        if request.user.role != 'user':
            return Response(
                {"detail": "Only users can subscribe"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            plan = FitnessPlan.objects.get(id=plan_id)
        except FitnessPlan.DoesNotExist:
            return Response({"detail": "Plan not found"}, status=404)

        subscription, created = Subscription.objects.get_or_create(
            user=request.user,
            plan=plan
        )

        if not created:
            return Response(
                {"message": "Already subscribed"},
                status=status.HTTP_200_OK
            )

        return Response(
            {"message": "Subscription successful"},
            status=status.HTTP_201_CREATED
        )
