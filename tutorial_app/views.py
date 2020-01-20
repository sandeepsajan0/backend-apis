from django.shortcuts import render
from .models import User
from rest_framework.views import APIView
from tutorial_app.serializers import (RegisterSerializer, MyTokenObtainPairSerializer)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
import jwt

class UserRegisterView(APIView):
    """
    API endpoint that allows user to be created.
    """
    def post(self, request, format=None):
        data =  request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            # serializer.save()
            tokens = MyTokenObtainPairSerializer.get_token(request.user)
            # print(type(tokens["jwt"]))
            # decodedPayload = jwt.decode(tokens["jwt"].encode, None, None)
            print(tokens)
            return Response(tokens)
        else:
            return Response({"bad request"})

class UserLoginView(APIView):
    """
    API endpoint that allows user to be logged in
    """
    def post(self, request, format=None):
        email = request.data['email']
        password = request.data['password']
        user = self.check_user(email, password)
        if user is not None:
            tokens = MyTokenObtainPairSerializer.get_token(request.user)
            return Response(tokens)
        return Response({"Not found"})

    def check_user(self, email, password):
        user = User.objects.filter(email=email)[0]
        if password == user.password:
            return True
        else:
            return False

# class UserTokenRefreshView(APIView):
#     """
#     API endpoint to get access token
#     """
#     def post(self, request, format=None):
#         refresh_token = request.data['refresh']
#         refresh_token = {"refresh": str.encode(refresh_token)}
#         print(refresh_token)
#         token = MyTokenObtainPairSerializer.get_access_token(refresh_token)
#         print(token)
#         return Response(token)

class UserDeleteView(APIView):
    """
    API endpoint to delete the user
    """
    def post(self, request, format=None):
        refresh = request.data['refresh']

class ProfileView(APIView):
    """
    API Endpoint for the current user profile
    """
    def get(self, request):
        token = request.headers['X-Access-Token']
        decodedPayload = jwt.decode(token, None, None)
        print(decodedPayload, request.user)
        # user  =request.user
        # print(user)
        # user = User.objects.get(email=user.email)
        # print(user)
        # email = user.email
        # name = user.name
        # avatar = user.avatar_url
        data = {'email':email, 'name':name, 'avatar':avatar}
        return Response(data)




