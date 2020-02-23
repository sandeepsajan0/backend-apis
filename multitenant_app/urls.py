from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.CompanyRegisterView.as_view(), name="register-company",),
    path("invitation/<str:token>/", views.ActivateUser.as_view()),
    path("login/", views.UserLoginView.as_view()),
    path("user/<int:pk>/", views.UserDetailsView.as_view()),
]
