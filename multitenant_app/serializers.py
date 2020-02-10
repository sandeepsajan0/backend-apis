from rest_framework import serializers
from .models import Company
from rest_framework_simplejwt.tokens import RefreshToken


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = Company
        fields = ["name", "password"]


class TokensObtainSerializer:
    @classmethod
    def get_token(cls, user):
        token = RefreshToken.for_user(user)
        return {
            "jwt": str(token.access_token),
        }
