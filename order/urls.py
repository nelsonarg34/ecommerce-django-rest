from django.urls import path, include
from rest_framework import routers
from order.views import OrderViewSet, OrderDetailViewSet, OrderFiltersViewSet, OrderDetailFiltersViewSet


router = routers.DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'orders_detail', OrderDetailViewSet)
router.register(r'orders_filters', OrderFiltersViewSet, basename = 'orders_filters')
router.register(r'orders_detail_filters', OrderDetailFiltersViewSet, basename = 'orders_detail_filters')

urlpatterns = [
    path('', include(router.urls)),
]