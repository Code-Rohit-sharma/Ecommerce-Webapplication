from rest_framework import serializers
from .models import ParentCategory, Category, CategoryMetaDataField, CategoryMetaDataFieldValue, Product, ProductVariation, ProductReview, Cart, Order, OrderProduct,Seller


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
        depth = 1


class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['product_variation', 'quantity', 'is_wishlist_item']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['customer_address_city', 'customer_address_state', 'customer_address_country',
                  'customer_address_address_line', 'customer_address_zip_code', 'customer_address_label', 'payment_method']


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = '__all__'
