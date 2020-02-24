from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    CompanyRegisterSerializer,
    UserRegisterSerializer,
    UserLoginSerializer,
    DocumentSerializer,
)
from .commands import get_activation_token, get_access_token
from django.core.exceptions import ObjectDoesNotExist
from _datetime import datetime
from calendar import timegm
import jwt
from .models import Company, User, Document
from .utils import tenant_from_request, is_company_user
from django.conf import settings
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

# Create your views here.


def get_activation_url(user, scheme, host):
    token = get_activation_token(user)
    company_name = user.company.url_prefix
    url = (
        scheme
        + "://"
        + str(company_name)
        + "."
        + str(host)
        + "/invitation/"
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
            for users in serializer.validated_data["user"]:
                username = users["username"]
                break
            user = User.objects.get(username=username)
            activation_url = get_activation_url(
                user, request.scheme, request.META["HTTP_HOST"]
            )
            message = Mail(
                from_email="sandeepsajan0@gmail.com",
                to_emails=[serializer.validated_data["user"][0]["email"]],
                subject="Sending the activation url",
                html_content="<a href={}> {}</a>".format(
                    activation_url, activation_url
                ),
            )
            try:
                sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
                response = sg.send(message)
            except Exception as e:
                response = {"ClientError": "{}".format(e)}

            return Response({"SendEmail": "Confirm your email address"})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ActivateUser(APIView):
    def get(self, request, token):
        """

        :param request:
        :return:
        """
        decodedPayload = jwt.decode(token, None, None)
        if timegm(datetime.now().timetuple()) < decodedPayload["exp"]:
            try:
                user_id = decodedPayload["user_id"]
                user = User.objects.get(id=user_id)
                user.is_active = True
                user.save()
                access_token = get_access_token(token)
            except Exception as e:
                return Response(
                    {"InvalidToken": "Error as {}".format(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response({"access": access_token}, status=status.HTTP_202_ACCEPTED)
        return Response({"ExpiredToken"}, status=status.HTTP_404_NOT_FOUND)


class UserLoginView(APIView):
    """

    """

    def post(self, request):
        company = tenant_from_request(request)
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(username=serializer.validated_data["username"])
            except:
                return Response(
                    {"ObjectDoesNotExist": "Invalid username"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            check__company_user = is_company_user(user, company)
            if check__company_user:
                if user.check_password(serializer.validated_data["password"]):
                    refresh_token = get_activation_token(user)
                    access_token = get_access_token(refresh_token)
                return Response(
                    {"refresh": refresh_token, "access": access_token},
                    status=status.HTTP_202_ACCEPTED,
                )
            else:
                return Response(
                    {"Validation Error": "Incorrect user or company details"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserDetailsView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserRegisterSerializer

    def get_object(self):
        queryset = User.objects.get(id=self.request.user.id)
        return queryset

    def delete(self, request, *args, **kwargs):
        user = request.user.id
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DocumentView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DocumentSerializer

    def post(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        company = tenant_from_request(request)
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, company=company)
            return Response(serializer.validated_data)

    def get_queryset(self):
        company = tenant_from_request(self.request)
        queryset = Document.objects.filter(user=self.request.user, company=company)
        return queryset


class DocumentDetailsView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()


#
# class AddUserView(APIView):
#     """
#     endpoint to add user to a company
#     """
#
#     def post(self, request, company_pk, token):
#         """
#
#         :param request:
#         :return:
#         """
#         decodedPayload = jwt.decode(token, None, None)
#         if timegm(datetime.now().timetuple()) < decodedPayload["exp"]:
#             serializer = UserRegisterSerializer(data=request.data)
#             if serializer.is_valid():
#                 try:
#                     company = Company.objects.get(id=company_pk)
#                     serializer.save(company=company)
#                 except ObjectDoesNotExist:
#                     raise
#                 return Response(status=status.HTTP_201_CREATED)
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         return Response(status=status.HTTP_403_FORBIDDEN)
