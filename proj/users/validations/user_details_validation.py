from users.models.user_details import UserDetails
from utils.validations.base_api_request_validation import \
    BaseApiRequestValidation
from utils.validations.request_validation import RequestValidation


class UserDetailsValidation(BaseApiRequestValidation):

    def login_validate(params):
        required_fields = ['email', 'password']
        RequestValidation.required_fields_validate(params, required_fields)
        email_exist = UserDetails.objects.filter(email__icontains=params.get("email"))
        if email_exist:
            password_exist = email_exist.filter(password=params.get("password"))
            if not password_exist:
                BaseApiRequestValidation.set_error('password', 'Invalid password!!')
        else:
            BaseApiRequestValidation.set_error('email', 'Invalid email id!!')