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
            'jwt': str(token.access_token),
            'refresh-token': str(token),
        }


class RegisterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'avatar_url']

    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)


class IdeasSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Idea
        fields = ('id','content', 'impact', 'ease', 'confidence', 'average_score', 'created_at')
