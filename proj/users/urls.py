from django.contrib import admin
from django.urls import path
from users.api_views.user_api_view import UserApiView


urlpatterns = [
    # -> APIs View
    path('register-api/', UserApiView.register),
    path('login-api/', UserApiView.login),
]