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

from .serializers import (
    OrderDetailSerializer,
    OrderSerializer,
    OrderDetailBasicSerializer,
    OrderDetailUpdateSerializer,
)
from .models import Order, OrderDetail
from .models import Product

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('buyer', 'order_items__product').all()
    serializer_class = OrderSerializer
    permission_classes = [
        permissions.IsAdminUser, permissions.IsAuthenticatedOrReadOnly, IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ['status']

    def get_queryset(self):
        user = self.request.user
        return Order.objects.prefetch_related('buyer','order_items__product').filter(buyer=user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        order_items = OrderDetail.objects.filter(order=instance.id).all()
        for item in order_items:
            product = Product.objects.filter(
                id=str(item.product)
            ).first()
            order_quantity = item.quantity
            product.stock += order_quantity
            product.save()

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.select_related('order', 'product').all()
    serializer_class = OrderDetailSerializer
    permission_classes = [
        permissions.IsAdminUser, permissions.IsAuthenticatedOrReadOnly, IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ['order__status', 'product__name']
   

    def get_queryset(self):
        user = self.request.user
        return OrderDetail.objects.select_related('order__buyer', 'product').filter(order__buyer=user)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_quantity = serializer.validated_data['quantity']
        user = self.request.user
        data = request.data

        product = Product.objects.get(
            id=data['product']
        )

        max_quantity = 5 # Esto podría implementarse como un campo en Product
        if order_quantity > max_quantity:
            raise exceptions.NotAcceptable("Quantity of this product not allowed.")

        if product.stock >= order_quantity:
            actual_quantity = product.stock
            product.stock = actual_quantity - order_quantity
            
        else:
            raise exceptions.NotAcceptable("Quantity of this product is out.")

        try:
            order = Order.objects.get(buyer=user, status="p")
            order_time = order.date_time + timedelta(minutes=60)
            now = datetime.now()
            now = pytz.utc.localize(now)

            if order_time < now:
                order.status="x"
                order.save(update_fields=['status'])
                order_items_detail = order.order_items.all()
                for item in order_items_detail:
                    product = Product.objects.filter(id=data['product']).first()
                    product.stock += item.quantity
                    product.save(update_fields=['stock'])
                    order.save()

                order = Order.objects.create(buyer=user, status="p")

        except ObjectDoesNotExist:
            order = Order.objects.create(buyer=user, status="p")
        orderdetail_serializer = self.get_queryset().filter(order=order)
        
        for order_product in orderdetail_serializer:
            if order_product.product == serializer.validated_data['product']:
                raise exceptions.NotAcceptable("The product exists in the order.")
            
        product.save(update_fields=['stock'])
        order_item = OrderDetail().create_order_item(order, product, order_quantity)
        serializer = OrderDetailBasicSerializer(order_item)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        max_quantity = 5 # Esto podría implementarse como un campo en Product
        order_quantity = request.data['quantity']
        print(order_quantity)
        if order_quantity > max_quantity:
            raise exceptions.NotAcceptable("Quantity of this product not allowed.")

        if instance.quantity != order_quantity:
            if order_quantity == 0:
               raise exceptions.NotAcceptable("The number of items to be added must be at least 1")
            else:
                product = Product.objects.get(id=str(instance.product))
                product.stock += instance.quantity - order_quantity
                if product.stock > 0:
                    product.save(update_fields=['stock'])
                else:
                    raise exceptions.NotAcceptable("Quantity of this product is out.")

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        product = Product.objects.filter(
            id=str(instance.product)
        ).order_by('created').first()

        order_quantity = instance.quantity
        product.stock += order_quantity
        product.save()

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

# Búsquedas y filtros (Django-filters)

class OrderFiltersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, 
                       filters.SearchFilter, filters.OrderingFilter]

    search_fields = ['buyer', 'status']
    ordering_fields = ['date_time', 'buyer']

    filterset_fields = {
    'buyer': ['exact'],
    'status': ['exact']
}

class OrderDetailFiltersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer
    filter_backends = [DjangoFilterBackend, 
                       filters.SearchFilter, filters.OrderingFilter]

    search_fields = ['order', 'product', 'created']
    ordering_fields = ['order', 'created']

    filterset_fields = {
    'order': ['exact'],
    'product': ['exact']
}