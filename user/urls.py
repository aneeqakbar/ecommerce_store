from django.urls import path,include
from django.conf.urls import url
from .views import (
    SignUpView,
    LogoutView,
    LoginView,
    AddAddressView,
    DetailUserView,
)

app_name = 'user'

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="SignUpView"),
    path("login/", LoginView.as_view(), name="LoginView"),
    path("logout/", LogoutView.as_view(), name="LogoutView"),
    path("add_address/", AddAddressView.as_view(), name="AddAddressView"),
    path("details/<pk>/", DetailUserView.as_view(), name="DetailUserView"),
]

