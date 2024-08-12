from django.conf import settings
from django.db.models import Q
from rest_framework import status as http_status
from networks.serializers.connects_details_serializer import ConnectsDetailsSerializer
from users.models.user_details import UserDetails
from networks.models.connects_details import ConnectsDetails
from users.serializers.user_details_serializer import UserDetailsSerializer, UserDetailsFriendsListSerializer
from users.services.user_details_service import UserDetailsService
from utils.api_response_util import ApiResponse, ApiResponseStatus
import uuid


class ConnectsRepository:


    def get_friends_list(request):
        '''
        Get List of Friends
        @request: request
        @response: dict api_status
        '''
        status_code, status, msg, data = http_status.HTTP_400_BAD_REQUEST, ApiResponseStatus.ERROR, [
            'Invalid request!'], None
        result = []
        token = request.token_payload
        _qry = request.GET.get("query", "")
        _page = int(request.GET.get("page", 1))
        _per_page = int(request.GET.get("per_page", 10))
        _from = (_page - 1) * _per_page
        _to = (_page) * _per_page
        user_details_objs = UserDetails.objects.filter(
            Q(first_name=_qry) |
            Q(last_name=_qry) |
            Q(email__icontains=_qry)
        ).exclude(id=token.get("user_id"))[_from:_to]
        user_details_serializer = UserDetailsFriendsListSerializer(user_details_objs, many=True)
        result = user_details_serializer.data
        if result:
            status_code = http_status.HTTP_200_OK
            status = ApiResponseStatus.SUCCESS
            msg = ['friends list retrived successfully.']
            data = result
        else:
            msg = ['friends list fetching process failed!!']

        return ApiResponse.api_status(status_code=status_code, status=status, message=msg, data=data)


    def get_friends_request_list(request):
        '''
        Get List of Friends Request
        @request: request
        @response: dict api_status
        '''
        status_code, status, msg, data = http_status.HTTP_400_BAD_REQUEST, ApiResponseStatus.ERROR, [
            'Invalid request!'], None
        result = []
        _send_to_id = 1
        _req_action = request.GET.get("action", "")
        
        _request_status = None
        if _req_action == "pending":
            _request_status = ConnectsDetails.RequestStautsType.PENDING
        elif _req_action == "accept":
            _request_status = ConnectsDetails.RequestStautsType.ACCEPT
        elif _req_action == "reject":
            _request_status = ConnectsDetails.RequestStautsType.REJECT
        
        _page = int(request.GET.get("page", 1))
        _per_page = int(request.GET.get("per_page", 10))
        _from = (_page - 1) * _per_page
        _to = (_page) * _per_page
        
        user_details_objs = ConnectsDetails.objects.filter(
            Q(send_to=_send_to_id) &
            Q(request_status=_request_status)
        )[_from:_to]
        user_details_serializer = ConnectsDetailsSerializer(user_details_objs, many=True)
        
        result = user_details_serializer.data
        if result:
            status_code = http_status.HTTP_200_OK
            status = ApiResponseStatus.SUCCESS
            msg = ['friends request list retrived successfully.']
            data = result
        else:
            msg = ['friends request list fetching process failed!!']

        return ApiResponse.api_status(status_code=status_code, status=status, message=msg, data=data)


    def send_connects(request):
        '''
        Register a User
        @request: request
        @response: dict api_status
        '''
        status_code, status, msg, data = http_status.HTTP_400_BAD_REQUEST, ApiResponseStatus.ERROR, [
            'Invalid request!'], None

        token_payload = request.token_payload

        _receive_to = request.data.get("receive_to_user_details_id")
        _send_to_obj = UserDetails.objects.filter(id=request.token_payload.get("user_id")).first()
        _receive_to_obj = UserDetails.objects.filter(id=_receive_to).first()
        result, is_created = ConnectsDetails.objects.get_or_create(
            send_to=_send_to_obj,
            receive_to=_receive_to_obj
        )

        if result:
            status_code = http_status.HTTP_200_OK
            status = ApiResponseStatus.SUCCESS
            msg = ['connection request send successfully.']
            data = {
                "connects_id": result.id,
            }
        else:
            msg = ['connection request sending failed!!']

        return ApiResponse.api_status(status_code=status_code, status=status, message=msg, data=data)


    def action_on_connects(request, id):
        '''
        Take a Action on Connects
        @request: request
        @response: dict api_status
        '''
        status_code, status, msg, data = http_status.HTTP_400_BAD_REQUEST, ApiResponseStatus.ERROR, [
            'Invalid request!'], None

        action = request.data.get('action')
        if action == "accept":
            _request_status = ConnectsDetails.RequestStautsType.ACCEPT
        else:
            _request_status = ConnectsDetails.RequestStautsType.REJECT

        # -> Fetch Connects Details
        result = ConnectsDetails.objects.filter(
            id = id
        ).update(
            request_status=_request_status
        )

        if result:
            status_code = http_status.HTTP_200_OK
            status = ApiResponseStatus.SUCCESS
            msg = ['action on connects taken successfully.']
        else:
            msg = ['action on connects getting failed!!']

        return ApiResponse.api_status(status_code=status_code, status=status, message=msg, data=data)
