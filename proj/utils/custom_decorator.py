from utils.api_request_util import ApiRequestUtil
from utils.api_response_util import ApiResponse


def auth_token_isvalid():
    # print(f'---auth_token_isvalid---')
    def inner_decorator(func):

        # print(f'---auth_token_isvalid--inner_decorator---')
        def wrapped(*args, **kwargs):
            
            # print(f'---auth_token_isvalid--wrapped---')
            auth_token = args[0].headers.get('auth-token')  # -> Check RestoAuthToken isValid..
            auth_token_result = ApiRequestUtil.auth_toekn_isvalid(auth_token)
            if auth_token_result.get("isvalid"):
                args[0]._mutable = True
                args[0].token_payload = auth_token_result.get("token_payload")
                result = func(*args, **kwargs)
            else:
                result = ApiResponse.api_response(message=[auth_token_result.get("reason")])
            return result

        return wrapped

    return inner_decorator