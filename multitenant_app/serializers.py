from rest_framework import serializers
from .models import Company, User, Document


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = super(UserRegisterSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.is_active = False
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super(UserRegisterSerializer, self).update(instance, validated_data)
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
            user = User.objects.create(
                company=company, owner_of_company=company, **data
            )
            user.set_password(data["password"])
            break
        user.is_superuser = True
        user.is_active = False
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=250, required=True)
    password = serializers.CharField(max_length=250, required=True)

    class Meta:
        model = User
        fields = ["username", "password"]


class DocumentSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source="user.username")
    company_name = serializers.ReadOnlyField(source="company.company_name")

    class Meta:
        model = Document
        fields = ["id", "doc_name", "doc_text", "user_name", "company_name"]
