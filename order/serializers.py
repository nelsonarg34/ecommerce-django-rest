from dataclasses import fields
from itertools import product
from rest_framework import serializers

from authentication.serializers import UserSerializer
from .models import Order, OrderDetail
from product.serializers import *


class OrderDetailMinSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderDetail
        fields = ['product']


class OrderDetailBasicSerializer(serializers.ModelSerializer):

    product_detail = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = OrderDetail
        fields = ['order', 'product', 'product_detail', 'quantity']


class OrderDetailBasicV1Serializer(serializers.ModelSerializer):

    product_detail = ProductBasicSerializer(source='product', read_only=True)
    order_item_total = serializers.ReadOnlyField(source='get_order_item_total')

    class Meta:
        model = OrderDetail
        fields = ['product', 'product_detail', 'quantity', 'order_item_total']


class OrderSerializer(serializers.ModelSerializer):

    buyer_detail = UserSerializer(source='buyer', read_only=True)
    order_items_detail = OrderDetailBasicV1Serializer(source='order_items',many=True, read_only=True)
    total = serializers.ReadOnlyField(source='get_total')
    total_usd = serializers.ReadOnlyField(source='get_total_usd')

    class Meta:
        model = Order
        fields = ['id', 'buyer', 'buyer_detail', 'order_items_detail','status', 'is_paid', 'date_time', 'total', 'total_usd']


class OrderBasicSerializer(serializers.ModelSerializer):

    buyer_detail = UserSerializer(source='buyer', read_only=True)
    total = serializers.ReadOnlyField(source='get_total')
    #total_usd = serializers.ReadOnlyField(source='get_total_usd')

    class Meta:
        model = Order
        fields = ['id', 'buyer_detail', 'status', 'is_paid', 'date_time', 'total']


class OrderDetailSerializer(serializers.ModelSerializer):
    
    product_detail = ProductBasicSerializer(source='product', read_only=True)
    order = OrderBasicSerializer(required=False, read_only=True)
    order_item_total = serializers.ReadOnlyField(source='get_order_item_total')

    class Meta:
        model = OrderDetail
        fields = ['id','order', 'product', 'product_detail', 'quantity', 'order_item_total']

class OrderDetailUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderDetail
        fields = ['quantity']



