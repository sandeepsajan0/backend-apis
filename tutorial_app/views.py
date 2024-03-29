import hashlib

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .commands import calculate_average_score
from .models import Idea, User
from .permissions import IsAuthorOwnerAdmin, add_user_to_group
from .serializers import (IdeasGetSerializer,  # ChangeGroupSerializer,
                          IdeasPostSerializer, RegisterSerializer,
                          UserLogoutSerializer, UserSerializer)


class UserRegisterView(APIView):
    """
    API endpoint for User Registration.
    "/users/"
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        """
        :param request:
        :param format:
        :return:
        """
        if request.user.is_superuser:
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
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
                    add_user_to_group(serializer.validated_data["user_group"], user)
                    return Response(
                        serializer.validated_data, status=status.HTTP_201_CREATED
                    )
                except ObjectDoesNotExist as e:
                    response = {"errors": ["UserDoesNotExist : {}".format(e)]}
                    return Response(response)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def put(self, request, format=None):
        """
        :param request:
        :param format:
        :return:
        """
        if request.user.is_superuser:
            if "email" in request.data:
                try:
                    user = User.objects.get(email=request.data["email"])
                except ObjectDoesNotExist as e:
                    response = {"errors": ["UserDoesNotExist : {}".format(e)]}
                    return Response(response)
                serializer = RegisterSerializer(user, data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    add_user_to_group(serializer.validated_data["user_group"], user)
                    return Response(
                        serializer.validated_data, status=status.HTTP_201_CREATED
                    )
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)


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
        if serializer.is_valid(raise_exception=True):
            token = RefreshToken(serializer.validated_data["refresh"])
            token.blacklist()
            return Response(status=status.HTTP_204_NO_CONTENT)


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
        if serializer.is_valid(raise_exception=True):
            average_score = calculate_average_score(serializer.validated_data)
            serializer.save(average_score=average_score, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class IdeaDetailView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint for details,update and destroy of an idea
    """

    permission_classes = [IsAuthenticated, IsAuthorOwnerAdmin]

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
            self.check_object_permissions(request, idea)
            serializer = IdeasPostSerializer(idea, data=request.data)
            if serializer.is_valid(raise_exception=True):
                average_score = calculate_average_score(serializer.validated_data)
                serializer.save(average_score=average_score)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            response = {"errors": ["UserDoesNotExist : {}".format(e)]}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            idea = Idea.objects.get(id=pk)
            self.check_object_permissions(request, idea)
            idea.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist as e:
            response = {"errors": ["UserDoesNotExist : {}".format(e)]}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
