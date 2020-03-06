from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    CompanyRegisterSerializer,
    UserRegisterSerializer,
    UserLoginSerializer,
    DocumentSerializer,
)
from _datetime import datetime
from calendar import timegm
import jwt
from .models import Company, User, Document
from .utils import get_activation_url, get_activation_token, get_access_token
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from django.utils.translation import gettext as _

# Create your views here.


class CompanyRegisterView(APIView):
    """
    View to Register a Company and a User simultaneously.
    Sending a mail on given email-id for activation purpose.
    """

    def post(self, request):
        serializer = CompanyRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            for users in serializer.validated_data["user"]:
                username = users["username"]
                break
            user = User.objects.get(username=username)
            activation_url = get_activation_url(
                user, request.scheme, request.META["HTTP_HOST"]
            )
            message = Mail(
                from_email=settings.FROM_EMAIL,
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
                return Response(response)

            return Response({"Success": "Confirm your email address"})


class ActivateUser(APIView):
    """
    View to handle the endpoint responsible for activate the user,
    Returns an access token
    """

    def post(self, request, token):
        decodedPayload = jwt.decode(token, None, None)
        if timegm(datetime.now().timetuple()) < decodedPayload["exp"]:
            try:
                user_id = decodedPayload["user_id"]
                user = User.objects.get(id=user_id)
                user.is_active = True
                user.save()
            except Exception as e:
                return Response(
                    {"InvalidToken": "Error as {}".format(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                {
                    "Success": "Hi {}, your account has been activated. You have to login to move forward.".format(
                        user.username
                    )
                },
                status=status.HTTP_202_ACCEPTED,
            )
        return Response({"Failed": "Token Expired"}, status=status.HTTP_404_NOT_FOUND)


class UserLoginView(APIView):
    """
    Login View for a user,
    Returns the refresh and the access tokens
    """

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                user = User.objects.get(
                    username=serializer.validated_data["username"],
                    company=request.company,
                )
            except:
                return Response(
                    {"ObjectDoesNotExist": "Invalid username"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            if user.check_password(serializer.validated_data["password"]):
                refresh_token = get_activation_token(user)
                access_token = get_access_token(refresh_token)
            return Response(
                {"refresh": refresh_token, "access": access_token},
                status=status.HTTP_202_ACCEPTED,
            )


class UserDetailsView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update and Destroy view for an authentic user
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = UserRegisterSerializer

    def get_object(self):
        queryset = User.objects.get(id=self.request.user.id)
        return queryset

    def delete(self, request, *args, **kwargs):
        user = request.user.id
        user.is_active = False
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DocumentView(ListCreateAPIView):
    """
    List and Create View for Documents by the authentic users under a company
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = DocumentSerializer

    def post(self, request, *args, **kwargs):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, company=request.company)
            return Response(serializer.validated_data)

    def get_queryset(self):
        company = self.request.company
        if self.request.user.owner_of_company == company:
            queryset = Document.objects.filter(company=company)
        else:
            queryset = Document.objects.filter(user=self.request.user, company=company)
        return queryset


class DocumentDetailsView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update and Destroy view for Document,
    Documents can only be accessed by the owner of company or author of documents.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = DocumentSerializer

    def get_object(self):
        company = self.request.company
        pk = self.kwargs.get("pk")
        if self.request.user.owner_of_company == company:
            queryset = Document.objects.filter(company=company, id=pk)
        else:
            queryset = Document.objects.filter(
                user=self.request.user, company=company, id=pk
            )
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(
                _("No %(verbose_name)s found matching the query")
                % {"verbose_name": queryset.model._meta.verbose_name}
            )
        return obj


class AddUserView(APIView):
    """
    View to add members(users) in a Comapny(tenant) by owner.
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        company = request.company
        if request.user.owner_of_company == company:
            serializer = UserRegisterSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(company=company)
                user = User.objects.get(username=serializer.validated_data["username"])
                activation_url = get_activation_url(
                    user, request.scheme, request.META["HTTP_HOST"]
                )
                message = Mail(
                    from_email=settings.FROM_EMAIL,
                    to_emails=[serializer.validated_data["email"]],
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
                    return Response(response)

                return Response({"Success": "Confirm your email address"})
        return Response(
            {"Validation Error": "Invalid user or company details"},
            status=status.HTTP_404_NOT_FOUND,
        )
