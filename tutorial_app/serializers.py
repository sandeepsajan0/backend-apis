from .models import User
from rest_framework import serializers
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class MyTokenObtainPairSerializer:
    @classmethod
    def get_token(cls, user):
        token = RefreshToken.for_user(user)
        return {
            'jwt': str(token.access_token),
            'refresh-token': str(token),
        }
    @classmethod
    def get_access_token(cls, refresh):
        token = RefreshToken(refresh)
        # print(token)
        return{
            {'jwt': str(refresh.access_token)}
        }


class RegisterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'avatar_url']

# class LoginSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['email', 'password']