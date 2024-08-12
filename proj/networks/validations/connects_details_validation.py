from networks.models.connects_details import ConnectsDetails
from users.models.user_details import UserDetails
from utils.date_time_util import DateTimeUtil
from utils.validations.base_api_request_validation import \
    BaseApiRequestValidation
from utils.validations.request_validation import RequestValidation


class ConnectsDetailsValidation(BaseApiRequestValidation):

    def action_on_connects_validate(params, token):
        required_fields = ['receive_to_user_details_id']
        RequestValidation.required_fields_validate(params, required_fields)
        
        _curr_dt = DateTimeUtil.get_current_datetime()
        _minus_mins_dt = DateTimeUtil.subtract_minutes_in_datetime(_curr_dt, 1)  # -> Minus 1 minute from current DateTime
        connects_count = ConnectsDetails.objects.filter(send_to=token.get("user_id"), created_at__gt = _minus_mins_dt).count()
        if connects_count > 3:
            BaseApiRequestValidation.set_error('receive_to_user_details_id', 'You can not send more then 3re request in a minute!!')