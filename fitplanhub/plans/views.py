from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import FitnessPlan
from .serializers import FitnessPlanSerializer
from accounts.permissions import IsTrainer

from subscriptions.utils import has_active_subscription
from rest_framework.permissions import IsAuthenticated
from follows.models import TrainerFollow
from subscriptions.models import Subscription


class TrainerPlanView(APIView):
    permission_classes = [IsAuthenticated, IsTrainer]

    def post(self, request):
        serializer = FitnessPlanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(trainer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        plans = FitnessPlan.objects.filter(trainer=request.user)
        serializer = FitnessPlanSerializer(plans, many=True)
        return Response(serializer.data)

class TrainerPlanDetailView(APIView):
    permission_classes = [IsAuthenticated, IsTrainer]

    def get_object(self, plan_id, user):
        try:
            return FitnessPlan.objects.get(id=plan_id, trainer=user)
        except FitnessPlan.DoesNotExist:
            return None

    def put(self, request, plan_id):
        plan = self.get_object(plan_id, request.user)
        if not plan:
            return Response({"detail": "Not found"}, status=404)

        serializer = FitnessPlanSerializer(plan, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, plan_id):
        plan = self.get_object(plan_id, request.user)
        if not plan:
            return Response({"detail": "Not found"}, status=404)

        plan.delete()
        return Response({"message": "Plan deleted"})

class PublicPlanListView(APIView):
    def get(self, request):
        plans = FitnessPlan.objects.select_related('trainer').all()

        data = []
        for plan in plans:
            data.append({
                "id": plan.id,
                "title": plan.title,
                "price": plan.price,
                "trainer": plan.trainer.name
            })

        return Response(data)

class PlanDetailView(APIView):
    def get(self, request, plan_id):
        try:
            plan = FitnessPlan.objects.select_related('trainer').get(id=plan_id)
        except FitnessPlan.DoesNotExist:
            return Response({"detail": "Not found"}, status=404)

        is_subscribed = False

        if request.user.is_authenticated and request.user.role == 'user':
            is_subscribed = has_active_subscription(request.user, plan)

        if is_subscribed:
            data = {
                "id": plan.id,
                "title": plan.title,
                "description": plan.description,
                "price": plan.price,
                "duration_days": plan.duration_days,
                "trainer": plan.trainer.name
            }
        else:
            data = {
                "id": plan.id,
                "title": plan.title,
                "price": plan.price,
                "trainer": plan.trainer.name
            }

        return Response(data)

class UserFeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'user':
            return Response(
                {"detail": "Feed is only available for users"},
                status=403
            )

        followed_trainers = TrainerFollow.objects.filter(
            user=request.user
        ).values_list('trainer_id', flat=True)

        plans = FitnessPlan.objects.select_related('trainer')\
            .filter(trainer_id__in=followed_trainers)

        subscribed_plan_ids = Subscription.objects.filter(
            user=request.user,
            is_active=True
        ).values_list('plan_id', flat=True)

        response_data = []

        for plan in plans:
            response_data.append({
                "plan_id": plan.id,
                "title": plan.title,
                "price": plan.price,
                "duration_days": plan.duration_days,
                "trainer": {
                    "id": plan.trainer.id,
                    "name": plan.trainer.name
                },
                "is_purchased": plan.id in subscribed_plan_ids
            })

        return Response(response_data)
