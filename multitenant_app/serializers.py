from rest_framework import serializers
from .models import Company, User
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]


class CompanySerializer(serializers.ModelSerializer):
    user = UserRegisterSerializer(many=True)

    class Meta:
        model = Company
        fields = [
            "company_name",
            "user",
        ]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        company = Company.objects.create(**validated_data)
        for data in user_data:
            user = User.objects.create(company=company, **data)
            user.set_password(data["password"])
            break
        user.save()
        return user


class TokensObtainSerializer:
    @classmethod
    def get_token(cls, user):
        token = RefreshToken.for_user(user)
        return str(token.access_token)
