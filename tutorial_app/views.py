from django.shortcuts import render
from .models import User, Idea
from rest_framework.views import APIView
from tutorial_app.serializers import (RegisterSerializer,
                                      MyTokenObtainPairSerializer,
                                      IdeasSerializer)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework import generics
from rest_framework.settings import api_settings
import urllib, hashlib
import jwt

class UserRegisterView(APIView):
    """
    API endpoint that allows user to be created.
    "/users/"
    """
    def post(self, request, format=None):
        data =  request.data
        _mutable = data._mutable
        data._mutable = True
        print(type(hashlib.md5(data['email'].encode('utf-8')).hexdigest()))
        gravatar_url = "https://www.gravatar.com/avatar/" + \
                       hashlib.md5(data['email'].encode('utf-8')).hexdigest() + "?"
        data['avatar_url'] = gravatar_url
        data._mutable = _mutable
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.filter(email=data['email'])[0]
            tokens = MyTokenObtainPairSerializer.get_token(user)
            decodedPayload = jwt.decode(str.encode(tokens["jwt"]), None, None)
            return Response(tokens, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

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
            return Response(tokens,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        refresh = request.data['refresh_token']
        decodedPayload = jwt.decode(refresh, None, None)
        user_id = decodedPayload['user_id']
        user = User.objects.get(id=user_id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
    # permission_classes = (IsAuthenticated,)
    def get(self, request):
        user_id = AuthenticateUser.get_user_id(request)
        user = User.objects.filter(id=user_id)[0]
        if user:
            email = user.email
            name = user.name
            avatar = user.avatar_url
            data = {'email':email, 'name':name, 'avatar':avatar}
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_302_FOUND)

class IdeasView(APIView):
    """
    API Endpoint for create and get ideas
    """
    def post(self, request, format=None):
        user_id = AuthenticateUser.get_user_id(request)
        user = User.objects.filter(id=user_id)
        if user:
            data = request.data
            serializer = IdeasSerializer(data=data)
            if serializer.is_valid():
                average_score = (data['ease'] + data['impact'] + data['confidence'])/3
                serializer.validated_data['average_score'] = average_score
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request):
        user_id = AuthenticateUser.get_user_id(request)
        user = User.objects.filter(id=user_id)
        if user:
            ideas = Idea.objects.all()
            pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
            paginator = pagination_class()
            page = paginator.paginate_queryset(ideas, request)
            print(page)
            serializer = IdeasSerializer(page, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class IdeaDetailView(APIView):
    """
    API endpoint for details and update of an idea
    """
    def get(self, request, pk):
        user_id = AuthenticateUser.get_user_id(request)
        user = User.objects.filter(id=user_id)
        if user:
            idea = Idea.objects.get(id=pk)
            serializer = IdeasSerializer(idea)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        user_id = AuthenticateUser.get_user_id(request)
        user = User.objects.filter(id=user_id)
        if user:
            data = request.data
            idea = Idea.objects.get(id=pk)
            serializer = IdeasSerializer(idea, data=data)
            if serializer.is_valid():
                average_score = (data['ease'] + data['impact'] + data['confidence'])/3
                serializer.validated_data['average_score'] = average_score
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, pk):
        user_id = AuthenticateUser.get_user_id(request)
        user = User.objects.filter(id=user_id)
        if user:
            idea = Idea.objects.get(id=pk)
            idea.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)



class AuthenticateUser:
    @classmethod
    def get_user_id(cls, request):
        token = request.headers['X-Access-Token']
        try:
            decodedPayload = jwt.decode(token, None, None)
            # print(decodedPayload['user_id'])
            user_id = decodedPayload['user_id']
            return user_id
        except:
            raise Exception




