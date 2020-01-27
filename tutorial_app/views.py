import hashlib
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, Idea
from tutorial_app.serializers import (RegisterSerializer,
                                      MyTokenObtainPairSerializer,
                                      IdeasSerializer)


class UserRegisterView(APIView):
    """
    API endpoint for User Registration.
    "/users/"
    """
    def post(self, request, format=None):
        """
        post method for register the user
        :param request:
        :param format:
        :return:
        """
        ## Not able to figure out what is happening in these lines. Can you explain?
        # data =  request.data
        # # doing this to add gravatar_url, if don't need it, comment next 5 lines(mutable).
        # _mutable = data._mutable
        # data._mutable = True
        # gravatar_url = "https://www.gravatar.com/avatar/" + \
        #                hashlib.md5(data['email'].encode('utf-8')).hexdigest() + "?"
        # data['avatar_url'] = gravatar_url
        # data._mutable = _mutable
        serializer = RegisterSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            # 1. Once you have valiated the serializer use seriliazer.validated_data for 
            # input data and not the request.data  So instead of data['email'] use 
            # serializer.validated_data.get("email")
            # 2. Instead of validating the user yourself, use django's authenticate method
            # 3. Never use index access bluntly. How will the below statement behave if there
            # is no user with this email? 
            user = User.objects.filter(email=data['email'])[0]
            tokens = MyTokenObtainPairSerializer.get_token(user)
            return Response(tokens, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLoginDeleteView(TokenObtainPairView, APIView,):
    """
    API endpoint that allows user to be logged in and logout the user
    Login can handle by TokenObtainPairView.
    "/access-token/"
    """
    def delete(self, request):
        """
        blacklist the user refresh token/ Logout user
        :param request:
        :return:
        """
        # serializer missing
        refresh = request.data['refresh']
        token = RefreshToken(refresh)
        token.blacklist()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileView(APIView):
    """
    API Endpoint for the current user profile
    ("/me/")
    """
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        """
        get the user profile
        :param request:
        :return:
        """
        # how are you getting the request.user?
        email = request.user.email
        name = request.user.name
        avatar = request.user.avatar_url
        # Create user model serializer, serializer user object and then return the reponse
        data = {'email':email, 'name':name, 'avatar':avatar}
        return Response(data, status=status.HTTP_200_OK)


class IdeasView(APIView):
    """
    API Endpoint for create and get ideas
    """
    permission_classes = (IsAuthenticated,)
    # Use ListCreate Generic API View
    def post(self, request, format=None):
        """
        post an idea by a user
        :param request:
        :param format:
        :return:
        """
        serializer = IdeasSerializer(data=request.data)

        if serializer.is_valid():
            average_score = (serializer.validated_data['ease'] +
                             serializer.validated_data['impact'] +
                             serializer.validated_data['confidence'])/3
            # do not change the validated_data dict
            # This can be achieved by serializer.save(average_score=average_score)
            serializer.validated_data['average_score'] = average_score
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    # This method is redundent and can be removed by the use of generic views
    def get(self, request):
        """
        get ideas with pagination 1page = 10ideas
        :param request:
        :return:
        """
        ideas = Idea.objects.all()
        pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
        paginator = pagination_class()
        page = paginator.paginate_queryset(ideas, request)
        serializer = IdeasSerializer(page, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class IdeaDetailView(APIView):
    # Replace this with RetrieveUpdateDestroyAPIView
    """
    API endpoint for details and update of an idea
    """
    permission_classes = (IsAuthenticated,)
    def get(self, request, pk):
        """
        get an specific idea's detail
        :param request:
        :param pk:
        :return:
        """
        # can throw DoesNotExistException Handle that
        idea = Idea.objects.get(id=pk)
        serializer = IdeasSerializer(idea)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        update an specific idea
        :param request:
        :param pk:
        :return:
        """
         # can throw DoesNotExistException Handle that
        idea = Idea.objects.get(id=pk)
        serializer = IdeasSerializer(idea, data=request.data)
        # The below steps are same as we have in post method
        # Use Mixin or some other way to remove duplicate code
        if serializer.is_valid():
            average_score = (serializer.validated_data['ease'] +
                             serializer.validated_data['impact'] +
                             serializer.validated_data['confidence'])/3
            serializer.validated_data['average_score'] = average_score
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        """
        delete an idea from the db
        :param request:
        :param pk:
        :return:
        """
         # can throw DoesNotExistException Handle that
         # Query can be changed to Idea.objects.filter(id=pk).delete()
        idea = Idea.objects.get(id=pk)
        idea.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)







