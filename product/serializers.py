from rest_framework import serializers
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    category = CategorySerializer(many=True)

    class Meta:
        model = Product
        fields = (
            "id", "name", "slug", "category", "price",
            "available", "stock", "created", "updated","image", "description")
    
    def to_representation(self,instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'category': instance.category.name,
            'description': instance.slug,
            'image': instance.image.url if instance.image != '' else '',
            'price': instance.price,
            'stock': instance.stock,
            'slug': instance.slug,
            'created': instance.created,
            'update': instance.updated,
        }

class ProductBasicSerializer(serializers.ModelSerializer):

    category = CategorySerializer(many=True)

    class Meta:
        model = Product
        fields = (
            "id", "name", "slug", "category", "price",
            "available", "stock", "created", "updated","image", "description")
    
    def to_representation(self,instance):
        return {
            'name': instance.name,
            'category': instance.category.name,
            'description': instance.slug,
            'image': instance.image.url if instance.image != '' else '',
            'price': instance.price,
        }