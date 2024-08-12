from django.contrib import admin
from users.models.user_details import UserDetails
from networks.models.connects_details import ConnectsDetails


class ConnectsDetailsAdmin(admin.ModelAdmin):
    list_display = ['id', 'send_to', 'receive_to', 'request_status', 'created_at']
    list_display_links = ('id', 'send_to', 'receive_to')
    search_fields = ('id', 'send_to', 'receive_to')
    readonly_fields=('send_to', 'receive_to')
    list_per_page = 20

admin.site.register(ConnectsDetails, ConnectsDetailsAdmin)

