from .models import User, Idea
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


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
        read_only_fields = ["avatar_url", "name", "email"]


class UserLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class IdeasPostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Idea
        fields = (
            "id",
            "content",
            "impact",
            "ease",
            "confidence",
            "average_score",
            "created_at",
        )
        read_only_fields = ["id", "average_score", "created_at"]

    def set_average_score(self, validated_data):
        average_score = (
            validated_data["ease"]
            + validated_data["impact"]
            + validated_data["confidence"]
        ) / 3
        return average_score


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
