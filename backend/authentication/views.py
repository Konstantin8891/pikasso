from authentication.serializers import (
    CustomTokenSerializer,
    LogoutSerializer,
    RegisterUserSerializer,
    UserViewSerializer,
)
from authentication.services import register_user
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import BlacklistedToken, OutstandingToken, RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer


class LogoutView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        now = timezone.now()
        BlacklistedToken.objects.filter(token__expires_at__lt=now).delete()
        OutstandingToken.objects.filter(expires_at__lt=now).delete()

        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                token = RefreshToken(request.data["refresh"])
                token.blacklist()
                return Response(status=status.HTTP_200_OK)
        except TokenError as e:
            raise InvalidToken(e.args[0])


class RegisterUser(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = register_user(serializer.validated_data)
        serializer = UserViewSerializer(instance=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
