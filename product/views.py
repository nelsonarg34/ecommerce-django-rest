from rest_framework import viewsets, permissions, status
from .models import Product, Category
from .serializers import (
    ProductSerializer, CategorySerializer)
from rest_framework.response import Response
from rest_framework import filters


class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [
        permissions.IsAdminUser, permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class ProductView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [
        permissions.IsAdminUser, permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'category__name']

    def get_queryset(self, pk=None):
        queryset = Product.available.all()
        return queryset

    def list(self, request):
        product_serializer = self.get_serializer(self.get_queryset(), many=True)
        data = {
            "total": self.get_queryset().count(),
            "totalNotFiltered": self.get_queryset().count(),
            "rows": product_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
