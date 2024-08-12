from utils.date_time_util import DateTimeUtil
from django.utils.translation import gettext_lazy as _
from networks.models.connects_details import ConnectsDetails
from users.models.user_details import UserDetails
from users.serializers.user_details_serializer import UserDetailsFriendsListSerializer
from rest_framework import serializers, validators


class ConnectsDetailsSerializer(serializers.ModelSerializer):

    receive_to = UserDetailsFriendsListSerializer()

    class Meta:
        model = ConnectsDetails
        fields = ("id", "receive_to", "request_status", "created_at")
