from .models import User, Idea
from rest_framework import serializers


class RegisterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["name", "email", "password", "user_group"]

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
