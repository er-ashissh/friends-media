from django.core.validators import (MinLengthValidator, MaxLengthValidator)
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models.user_details import UserDetails
from utils.models.base import Base


class ConnectsDetails(models.Model):

    class RequestStautsType(models.IntegerChoices):
        PENDING = 0, _("Pending")
        ACCEPT = 1, _("Accept")
        REJECT = 2, _("Reject")

    send_to = models.ForeignKey(UserDetails, related_name="send_to_related", on_delete=models.DO_NOTHING)
    receive_to = models.ForeignKey(UserDetails, related_name="receive_to_related", on_delete=models.DO_NOTHING)
    request_status = models.IntegerField(choices=RequestStautsType.choices, default=RequestStautsType.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return f"{self.send_to}_to_{self.send_to}_{self.request_status}"
    
    class Meta:
        unique_together = [['send_to', 'receive_to']]
        ordering = ['-id']