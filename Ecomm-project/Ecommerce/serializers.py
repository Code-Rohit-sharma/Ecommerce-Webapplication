from rest_framework import serializers
from .models import ParentCategory, Category, CategoryMetaDataField, CategoryMetaDataFieldValue, Product, ProductVariation, ProductReview


class ParentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentCategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryMetaDataFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryMetaDataField
        fields = '__all__'


class CategoryMetaDataFieldValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryMetaDataFieldValue
        fields = '__all__'
        depth = 1


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductVariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariation
        fields = '__all__'


class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = '__all__'
