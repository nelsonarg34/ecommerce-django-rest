from django.db import models
from django.db import connection
from tenant_schemas.models import TenantMixin


class Client(TenantMixin):
    name = models.CharField(max_length=100)
    on_trial = models.BooleanField()
    created_on = models.DateField(auto_now_add=True)
    auto_create_schema = True

    def __str__(self):
        return self.name

    def get_current_tenant():
        """Return current tenant based on schema_name."""
        schema_name = connection.schema_name
        return schema_name
