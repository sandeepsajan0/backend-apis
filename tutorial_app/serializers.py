from .models import User, Idea
from rest_framework import serializers

# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import HTTP_HEADER_ENCODING


class MyTokenObtainPairSerializer:
    @classmethod
    def get_token(cls, user):
        token = RefreshToken.for_user(user)
        return {
            "jwt": str(token.access_token),
            "refresh-token": str(token),
        }


class RegisterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["name", "email", "password"]

    def create(self, validated_data):
        user = super(RegisterSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["name", "email", "avatar_url"]


class UserLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class IdeasPostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Idea
        fields = (
            "content",
            "impact",
            "ease",
            "confidence",
        )


class IdeasGetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Idea
        fields = [
            "id",
            "content",
            "impact",
            "ease",
            "confidence",
            "average_score",
            "created_at",
        ]
