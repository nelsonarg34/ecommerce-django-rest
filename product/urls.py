from django.urls import path, include
from rest_framework import routers
from product.views import ProductView, CategoryView

router = routers.DefaultRouter()
router.register(r'products', ProductView, basename='products')
router.register(r'categories', CategoryView)

urlpatterns = [
    path('', include(router.urls)),
]