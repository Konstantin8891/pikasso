from bicycles.models import Bicycle
from bicycles.serializers import (
    BicycleCreateSerializer,
    BicycleRentSerializer,
    BicycleViewSerializer,
    RentHistorySerializer,
)
from bicycles.services import create_bicycle, finish_rent, start_rent
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import UserBill


class BicycleCreateListView(ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Bicycle.objects.filter(user__isnull=True).order_by("id")

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BicycleCreateSerializer
        return BicycleViewSerializer

    def post(self, request, *args, **kwargs):  # Вспомогательный эндпоинт, в ТЗ этого нет
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bicycle = create_bicycle(serializer.validated_data)
        serializer = BicycleViewSerializer(instance=bicycle)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RentView(CreateAPIView):
    serializer_class = BicycleRentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data["rent"]:
            start_rent(serializer.validated_data["bicycle"], request.user)
        else:
            finish_rent(serializer.validated_data["bicycle"], request.user)
        return Response(status=status.HTTP_200_OK)


class RentHistoryView(ListAPIView):
    serializer_class = RentHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserBill.objects.filter(user=self.request.user)
