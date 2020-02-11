from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CompanySerializer, TokensObtainSerializer
from .models import Company, User

# Create your views here.


class CompanyRegisterView(APIView):
    """
    Endpoint for Register an User.
    """

    def post(self, request):
        """

        :param request:
        :return:
        """
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(
                username=serializer.validated_data["user"][0]["username"]
            )
            token = TokensObtainSerializer.get_token(user)
            company_id = Company.objects.get(
                company_name=serializer.validated_data["company_name"]
            ).id
            url = (
                request.scheme
                + "://"
                + str(request.META["HTTP_HOST"])
                + "/mt-app/invitation/"
                + str(company_id)
                + "/"
                + str(token)
            )
            return Response({"invitation": url})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class AddUserView(APIView):
    """
    endpoint to add user to a company
    """

    def post(self, request):
        """

        :param request:
        :return:
        """
