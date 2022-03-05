from django.db import connection
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.contrib import admin

from .models import Client

class BasePublicOnlyAdmin(admin.ModelAdmin):
    """
    This mixin shows the admin section only in
    the public tenant admin's page
    """

    def get_queryset(self, request):
        """
        No other schema apart from the public is allowed to view tenants.
        """
        current_tenant = connection.tenant
        if current_tenant.schema_name == settings.PUBLIC_SCHEMA_NAME:
            return super(BasePublicOnlyAdmin, self).get_queryset(request)
        else:
            raise PermissionDenied

    def get_model_perms(self, request):
        """
        No other schema apart from the public is allowed to view,
        add, change or delete other tenants.
        """
        is_allowed = False
        current_tenant = connection.tenant

        if current_tenant.schema_name == settings.PUBLIC_SCHEMA_NAME:
            is_allowed = True
        return {
            'add': is_allowed,
            'change': is_allowed,
            'delete': is_allowed,
            'view': is_allowed,
        }

admin.site.register(Client, BasePublicOnlyAdmin)