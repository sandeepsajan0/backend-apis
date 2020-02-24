from django.urls import include, path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("", views.CompanyRegisterView.as_view(), name="register-company",),
    path("invitation/<str:token>/", views.ActivateUser.as_view()),
    path("login/", views.UserLoginView.as_view()),
    path("me/", views.UserDetailsView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("doc/", views.DocumentView.as_view()),
    path("doc/<int:pk>", views.DocumentDetailsView.as_view()),
]
