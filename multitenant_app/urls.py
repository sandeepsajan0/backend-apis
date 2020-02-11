from django.urls import include, path
from . import views

urlpatterns = [
    path(
        "register-company/",
        views.CompanyRegisterView.as_view(),
        name="register-company",
    ),
    path("invitation/<int>/<string>/", views.AddUserView.as_view()),
]
