from django.contrib import admin
from django.urls import path
from networks.api_views.connects_api_view import ConnectsApiView


urlpatterns = [
    # -> APIs View
    path('friends-list-api/', ConnectsApiView.friends_list),
    path('friends-request-list-api/', ConnectsApiView.friends_request_list),
    path('send-connects-api/', ConnectsApiView.send_connects),
    path('action-on-connects-api/<int:id>/', ConnectsApiView.action_on_connects),
]