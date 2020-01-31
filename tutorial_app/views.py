import hashlib
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, Idea
from tutorial_app.serializers import (
    RegisterSerializer,
    IdeasPostSerializer,
    IdeasGetSerializer,
    UserLogoutSerializer,
    UserSerializer,
)
from .commands import get_token, calculate_average_score


class UserRegisterView(APIView):
    """
    API endpoint for User Registration.
    "/users/"
    """

    def post(self, request, format=None):
        """
        :param request:
        :param format:
        :return:
        """
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            gravatar_url = (
                "https://www.gravatar.com/avatar/"
                + hashlib.md5(
                    serializer.validated_data["email"].encode("utf-8")
                ).hexdigest()
                + "?"
            )
            serializer.save(avatar_url=gravatar_url)
            try:
                user = User.objects.get(email=serializer.validated_data["email"])
                tokens = get_token(user)
                return Response(tokens, status=status.HTTP_201_CREATED)
            except ObjectDoesNotExist:
                raise
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLoginDeleteView(
    TokenObtainPairView, APIView,
):
    """
    API endpoint for login and logout of a user
    Login can handle by TokenObtainPairView.
    "/access-token/"
    """

    def delete(self, request):
        """
        blacklist the user refresh token/ Logout user
        :param request:
        :return:
        """
        serializer = UserLogoutSerializer(data=request.data)
        if serializer.is_valid():
            token = RefreshToken(serializer.validated_data["refresh"])
            token.blacklist()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    """
    API Endpoint for the current user's profile
    ("/me/")
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        get the user profile
        :param request:
        :return:
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class IdeasView(ListCreateAPIView):
    """
    API Endpoint for create ideas and get ideas with pagination
    """

    permission_classes = (IsAuthenticated,)

    serializer_class = IdeasGetSerializer
    queryset = Idea.objects.all()

    def post(self, request, format=None):
        """
        post an idea by a user
        :param request:
        :param format:
        :return:
        """
        serializer = IdeasPostSerializer(data=request.data)
        if serializer.is_valid():
            average_score = calculate_average_score(serializer.validated_data)
            serializer.save(average_score=average_score, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class IdeaDetailView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint for details,update and destroy of an idea
    """

    permission_classes = (IsAuthenticated,)

    serializer_class = IdeasGetSerializer
    queryset = Idea.objects.all()

    def put(self, request, pk):
        """
        update an idea
        :param request:
        :param pk:
        :return:
        """
        try:
            idea = Idea.objects.get(id=pk)
            if idea.author == request.user:
                serializer = IdeasPostSerializer(idea, data=request.data)
                if serializer.is_valid():
                    average_score = calculate_average_score(serializer.validated_data)
                    serializer.save(average_score=average_score)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_403_FORBIDDEN)
        except ObjectDoesNotExist:
            raise

    def delete(self, request, pk):
        try:
            idea = Idea.objects.get(id=pk)
            if idea.author == request.user:
                idea.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_403_FORBIDDEN)
        except ObjectDoesNotExist:
            raise
