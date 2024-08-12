from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from users.repositories.user_repository import UserRepository
from networks.repositories.connects_repository import ConnectsRepository
from networks.validations.connects_details_validation import ConnectsDetailsValidation
from utils.api_response_util import ApiResponse
from utils.custom_decorator import auth_token_isvalid
from utils.validations.bell_validation import BellValidation
from users.validations.user_details_validation import UserDetailsValidation
from utils.validations.base_api_request_validation import BaseApiRequestValidation

import logging


class ConnectsApiView(APIView):

    @api_view(['GET'])
    @auth_token_isvalid()
    @transaction.atomic
    def friends_list(request):
        result = ConnectsRepository.get_friends_list(request)
        return ApiResponse.api_response(**result)


    @api_view(['GET'])
    @auth_token_isvalid()
    @transaction.atomic
    def friends_request_list(request):
        result = ConnectsRepository.get_friends_request_list(request)
        return ApiResponse.api_response(**result)


    @api_view(['POST'])
    @auth_token_isvalid()
    @transaction.atomic
    def send_connects(request):
        BaseApiRequestValidation.clear_error()
        ConnectsDetailsValidation.action_on_connects_validate(request.data, request.token_payload)
        BellValidation.check_has_error()

        result = ConnectsRepository.send_connects(request)
        return ApiResponse.api_response(**result)


    @api_view(['PUT'])
    @auth_token_isvalid()
    @transaction.atomic
    def action_on_connects(request, id):
        result = ConnectsRepository.action_on_connects(request, id)
        return ApiResponse.api_response(**result)



