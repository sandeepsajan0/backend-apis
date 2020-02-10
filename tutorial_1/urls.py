"""tutorial_1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.contrib import admin
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_swagger.views import get_swagger_view
import os

schema_view = get_swagger_view(title="Pastebin API")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
if os.getenv("DJANGO_SETTINGS_MODULE") == "tutorial_1.settings.multitenant_app":
    urlpatterns = [
        path("", schema_view),
        path("admin/", admin.site.urls),
        path("mt-app/", include("multitenant_app.urls")),
    ]
else:
    from tutorial_app import views

    urlpatterns = [
        path("admin/", admin.site.urls),
        path("assign-group/", views.AssignGroup.as_view(), name="assign_group"),
        path("access-token/", views.UserLoginDeleteView.as_view(), name="user_login"),
        path("access-token/refresh/", TokenRefreshView.as_view(), name="refresh_token"),
        path("users/", views.UserRegisterView.as_view(), name="create_user"),
        path("me/", views.ProfileView.as_view(), name="user_profile"),
        path("ideas/", views.IdeasView.as_view(), name="ideas"),
        path("ideas/<int:pk>/", views.IdeaDetailView.as_view(), name="particular_idea"),
        path("", schema_view),
    ]
