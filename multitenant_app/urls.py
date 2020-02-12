from django.urls import include, path
from . import views

urlpatterns = [
    path(
        "register-company/",
        views.CompanyRegisterView.as_view(),
        name="register-company",
    ),
    path("login-company/", views.CompanyLoginView.as_view()),
    path("invitation/<int:company_pk>/<str:token>/", views.AddUserView.as_view()),
]
