from rest_framework import serializers
from .models import Company, User
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = super(UserRegisterSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class CompanyRegisterSerializer(serializers.ModelSerializer):
    user = UserRegisterSerializer(many=True)

    class Meta:
        model = Company
        fields = [
            "company_name",
            "url_prefix",
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


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=250)

    class Meta:
        model = User
        fields = ["username", "password"]


# class CompanyLoginSerializer(serializers.Serializer):
#     user = UserLoginSerializer(many=True)
#
#     class Meta:
#         model = Company
#         fields = [
#             "company_name",
#             "user",
#         ]


class TokensObtainSerializer:
    @classmethod
    def get_token(cls, user):
        token = RefreshToken.for_user(user)
        return str(token.access_token)
