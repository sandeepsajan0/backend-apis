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
    "/users/"
    """
    def post(self, request, format=None):
        data =  request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.filter(email=data['email'])[0]
            tokens = MyTokenObtainPairSerializer.get_token(user)
            decodedPayload = jwt.decode(str.encode(tokens["jwt"]), None, None)
            return Response(tokens)
        else:
            return Response({"bad request"})

class UserLoginDeleteView(APIView):
    """
    API endpoint that allows user to be logged in
    "/access-token/"
    """
    def post(self, request, format=None):
        email = request.data['email']
        password = request.data['password']
        user = self.check_user(email, password)
        if user is not None:
            tokens = MyTokenObtainPairSerializer.get_token(request.user)
            return Response(tokens)
        return Response({"Not found"})

    def delete(self, request):
        refresh = request.data['refresh_token']
        decodedPayload = jwt.decode(refresh, None, None)
        user_id = decodedPayload['user_id']
        user = User.objects.get(id=user_id)
        user.delete()
        return Response("204")


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
#         refresh_token = request.data['refresh_token']
#         refresh_token_byte = str.encode(refresh_token)
#         print(type(refresh_token_byte))
#         token = MyTokenObtainPairSerializer.get_access_token(refresh_token_byte)
#         print(token)
#         return Response(token)

class ProfileView(APIView):
    """
    API Endpoint for the current user profile
    ("/me/")
    """
    def get(self, request):
        token = request.headers['X-Access-Token']
        decodedPayload = jwt.decode(token, None, None)
        # print(decodedPayload['user_id'])
        user_id = decodedPayload['user_id']
        user = User.objects.get(id=user_id)
        email = user.email
        name = user.name
        avatar = user.avatar_url
        data = {'email':email, 'name':name, 'avatar':avatar}
        return Response(data)




