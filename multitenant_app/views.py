from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    CompanyRegisterSerializer,
    TokensObtainSerializer,
    UserRegisterSerializer,
    CompanyLoginSerializer,
)
from django.core.exceptions import ObjectDoesNotExist
from _datetime import datetime
from calendar import timegm
import jwt
from .models import Company, User

# Create your views here.


def get_invitation_url(data, scheme, host):
    for users in data["user"]:
        username = users["username"]
        break
    user = User.objects.get(username=username)
    token = TokensObtainSerializer.get_token(user)
    company_id = user.company.id
    url = (
        scheme
        + "://"
        + str(host)
        + "/mt-app/invitation/"
        + str(company_id)
        + "/"
        + str(token)
    )
    return url


class CompanyRegisterView(APIView):
    """
    Endpoint for Register an User.
    """

    def post(self, request):
        """

        :param request:
        :return:
        """
        serializer = CompanyRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            url = get_invitation_url(
                serializer.validated_data, request.scheme, request.META["HTTP_HOST"]
            )
            return Response({"invitation": url})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CompanyLoginView(APIView):
    """

    """

    def post(self, request):
        serializer = CompanyLoginSerializer(data=request.data)
        if serializer.is_valid():
            url = get_invitation_url(
                request.data, request.scheme, request.META["HTTP_HOST"],
            )
            return Response({"invitation": url})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class AddUserView(APIView):
    """
    endpoint to add user to a company
    """

    def post(self, request, company_pk, token):
        """

        :param request:
        :return:
        """
        decodedPayload = jwt.decode(token, None, None)
        if timegm(datetime.now().timetuple()) < decodedPayload["exp"]:
            serializer = UserRegisterSerializer(data=request.data)
            if serializer.is_valid():
                try:
                    company = Company.objects.get(id=company_pk)
                    serializer.save(company=company)
                except ObjectDoesNotExist:
                    raise
                return Response(status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)
