from django.db import models
from django.utils.translation import gettext_lazy as _
# from resto_app.models.user_details import UserDetails


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # created_by = models.CharField(default='system', max_length=255)
    # created_by = models.ForeignKey('resto_app.UserDetails', null=True, blank=True, related_name="created_by_%(class)s_set", on_delete=models.DO_NOTHING)
    # updated_by = models.CharField(default='system', max_length=255)
    # updated_by = models.ForeignKey('resto_app.UserDetails', null=True, blank=True, related_name="updated_by_%(class)s_set", on_delete=models.DO_NOTHING)
    
    class Meta:
        abstract = True


class StatusBase(models.Model):

    class StautsType(models.IntegerChoices):
        DISABLE = 0, _("Disable")
        ENABLE = 1, _("Enable")
        DELETED = 2, _("Deleted")

    status = models.IntegerField(choices=StautsType.choices, default=StautsType.ENABLE)

    class Meta:
        abstract = True
