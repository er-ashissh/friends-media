from django.conf import settings
from rest_framework import status as http_status
from users.models.user_details import UserDetails
from users.services.user_details_service import UserDetailsService
from utils.api_response_util import ApiResponse, ApiResponseStatus
from utils.date_time_util import DateTimeUtil
from utils.encode_decode_string import encode_json
import uuid


class UserRepository:
    
    def register(request):
        '''
        Register a User
        @request: request
        @response: dict api_status
        '''
        status_code, status, msg, data = http_status.HTTP_400_BAD_REQUEST, ApiResponseStatus.ERROR, [
            'Invalid request!'], None

        result = UserDetailsService.create(request.data)
        if result:
            status_code = http_status.HTTP_200_OK
            status = ApiResponseStatus.SUCCESS
            msg = ['User register successfully.']
            data = {
                "user_id": result,
            }
        else:
            msg = ['User registration failed!!']

        return ApiResponse.api_status(status_code=status_code, status=status, message=msg, data=data)


    def login(request):
        '''
        Login a User
        @request: request
        @response: dict api_status
        '''
        status_code, status, msg, data = http_status.HTTP_400_BAD_REQUEST, ApiResponseStatus.ERROR, [
            'Invalid request!'], None

        # -> Check User login Credentials..
        _email = request.data.get("email")
        _pwd = request.data.get("password")
        user_exist = UserDetails.objects.filter(email__icontains=_email, password=_pwd, status=UserDetails.StautsType.ENABLE).first()
        if user_exist:
            _current_dt = DateTimeUtil.get_current_datetime()
            _new_dt = DateTimeUtil.add_day_in_datetime(_current_dt, 2)  # -> AuthToken is valid for 2 days
            _clean_dt = DateTimeUtil.rm_hyphen_from_datetime(_new_dt)
            jwt_token_payload = {
                "user_id": user_exist.id,
                "user_first_name": user_exist.first_name,
                "user_last_name": user_exist.last_name,
                "user_full_name": user_exist.get_full_name(),
                "user_email": user_exist.email,
                "login_created_at": DateTimeUtil.get_datetime_int(),
                "token_valid_till": _clean_dt
            }
            auth_jwt_token = encode_json(jwt_token_payload)

            status_code = http_status.HTTP_200_OK
            status = ApiResponseStatus.SUCCESS
            msg = ['User logged-in successfully.']
            data = {
                "user_id": user_exist.id,
                "auth_token": auth_jwt_token,
                "token_payload": jwt_token_payload,
            }
        else:
            msg = ['Invalid login credentials!!']

        return ApiResponse.api_status(status_code=status_code, status=status, message=msg, data=data)
