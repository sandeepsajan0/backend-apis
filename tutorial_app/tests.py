from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User
from .serializers import RegisterSerializer, IdeasPostSerializer


class BaseTest(APITestCase):
    def setUp(self):
        """

        :return:
        """
        self.access_token = ""
        user_data = {
            "email": "test@gmail.com",
            "name": "test_name",
            "password": "test@123",
        }
        idea_data = {
            "content": "Ultimate Test Content",
            "impact": 5,
            "ease": 3,
            "confidence": 7,
        }
        user_serializer = RegisterSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
        idea_serializer = IdeasPostSerializer(data=idea_data)
        if idea_serializer.is_valid():
            idea_serializer.save(average_score=5)
            print(idea_serializer.data["id"])

    def get_token(self):
        login_url = reverse("user_login")
        login_data = {"email": "test@gmail.com", "password": "test@123"}
        login_response = self.client.post(login_url, login_data, format="json")
        access_token = login_response.data["access"]
        refresh_token = login_response.data["refresh"]
        return {"access": access_token, "refresh": refresh_token}

    def test_create_user(self):
        """

        :return:
        """
        url = reverse("create_user")
        data = {
            "name": "test_name1",
            "email": "test1@gmail.com",
            "password": "test@123",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        """

        :return:
        """
        url = reverse("user_login")
        data = {"email": "test@gmail.com", "password": "test@123"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_profile(self):
        """

        :return:
        """
        tokens = self.get_token()
        url = reverse("user_profile")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + tokens["access"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "test@gmail.com")

    def test_refresh_token(self):
        """

        :return:
        """
        tokens = self.get_token()
        url = reverse("refresh_token")
        data = {"refresh": tokens["refresh"]}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ideas_post(self):
        """

        :return:
        """
        tokens = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + tokens["access"])
        url = reverse("ideas")
        data = {"content": "Test_content", "impact": 6, "ease": 6, "confidence": 6}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["content"], "Test_content")
        self.assertEqual(response.data["average_score"], (6 + 6 + 6) / 3)

    def test_ideas_get(self):
        """

        :return:
        """
        tokens = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + tokens["access"])
        url = reverse("ideas")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_idea_get(self):
        """

        :return:
        """
        tokens = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + tokens["access"])
        response = self.client.get("/ideas/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_idea_put(self):
        """

        :return:
        """
        tokens = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + tokens["access"])
        data = {
            "content": "Changed Test Content",
            "impact": 5,
            "ease": 3,
            "confidence": 7,
        }
        response = self.client.put("/ideas/1/", data, format=None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], "Changed Test Content")

    def test_idea_delete(self):
        """

        :return:
        """
        tokens = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + tokens["access"])
        response = self.client.delete("/ideas/1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_logout(self):
        """

        :return:
        """
        tokens = self.get_token()
        url = reverse("user_login")
        data = {"refresh": tokens["refresh"]}
        response = self.client.delete(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
