from datetime import datetime
from datetime import timedelta
import pytz

from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import filters
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework import permissions, status, exceptions
from django_filters.rest_framework import DjangoFilterBackend

from cart.models import Cart 

from .serializers import (
    CartSerializer,
)
from order.models import Order, OrderDetail
from product.models import Product

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.select_related('order').all()
    serializer_class = CartSerializer
    permission_classes = [
        permissions.IsAdminUser, permissions.IsAuthenticatedOrReadOnly, IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ['order']
'''
    def get_queryset(self):
        user = self.request.user
        return Cart.objects.select_related('order').filter(order__buyer=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_id = serializer.validated_data['order']
        user = self.request.user
        data = request.data

        order_items = OrderDetail.objects.get(order=order_id)

        product = Product.objects.get(
            id=data['product']
      )'''

