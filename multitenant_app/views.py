from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CompanySerializer, TokensObtainSerializer
from .models import Company

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
            company = Company.objects.get(name=serializer.validated_data["name"])
            token = TokensObtainSerializer.get_token(company)
            return Response({"access": token})
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return HttpResponse("yes working")
