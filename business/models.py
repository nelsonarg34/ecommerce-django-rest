from django.db import models
from django.db import connection
from tenant_schemas.models import TenantMixin

from business.constants import (
    BUSINESS_ECOMMERCE_TYPE_CHOICES,
    BUSINESS_TO_CONSUMER,
    COUNTRY_CHOICES,
    ARGENTINA,
)


class Client(TenantMixin):
    name = models.CharField(max_length=150)
    type_of_business = models.CharField(max_length=30, choices=BUSINESS_ECOMMERCE_TYPE_CHOICES, default=BUSINESS_TO_CONSUMER)
    country = models.CharField(max_length=30, choices=COUNTRY_CHOICES, default=ARGENTINA)
    on_trial = models.BooleanField()
    created_on = models.DateField(auto_now_add=True)
    auto_create_schema = True

    class Meta:
        ordering = ('name',)
        verbose_name = 'client'
        verbose_name_plural = 'clients'

    def __str__(self):
        return self.name

