from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.models import User


class CustomTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        attrs["email"] = attrs["email"].lower()
        return super().validate(attrs)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "email", "password")

    def validate(self, attrs):
        attrs["email"] = attrs["email"].lower()
        return attrs


class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name", "email")
