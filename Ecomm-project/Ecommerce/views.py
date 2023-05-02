from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import ParentCategorySerializer, CategorySerializer, CategoryMetaDataFieldSerializer, CategoryMetaDataFieldValueSerializer, ProductSerializer, ProductVariationSerializer, ProductReviewSerializer, CartSerializer, OrderSerializer, OrderProductSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import ParentCategory, Category, CategoryMetaDataField, CategoryMetaDataFieldValue, Product, ProductVariation, ProductReview, Cart, Order, OrderProduct, OrderStatus
from rest_framework.permissions import AllowAny
from usersapp.models import Customer
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class ParentCategoryView(APIView):

    def get(self, request):
        parentcategorydata = ParentCategory.objects.filter(is_active=True)
        serializer = ParentCategorySerializer(parentcategorydata, many=True)
        return Response({
            'data': serializer.data
        })

    def post(self, request):
        data = request.data
        serializer = ParentCategorySerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response({
            'message': 'data saved',
            'status': status.HTTP_200_OK
        })

    def delete(self, request):
        data = request.data
        try:
            parent_category = ParentCategory.objects.get(
                parent_category_name=data['parent_category_name'])
        except:
            return Response({
                'message': 'parent category with this name is not exists..!!!',
                'status': status.HTTP_400_BAD_REQUEST
            })

        if parent_category.is_delete == True:
            return Response({
                'message': 'category is already deleted',
                'status': status.HTTP_400_BAD_REQUEST
            })
        parent_category.is_delete = True
        parent_category.save()
        return Response({
            'message': 'category deleted',
            'status': status.HTTP_200_OK
        })


class CategoryView(APIView):

    def get(self, request):
        category = Category.objects.filter(is_active=True)
        serializer = CategorySerializer(category, many=True)
        return Response({
            'data': serializer.data
        })

    def post(self, request):
        data = request.data
        serializer = CategorySerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response({
            'message': 'data saved',
            'status': status.HTTP_200_OK
        })

    def delete(self, request):
        data = request.data
        try:
            category = Category.objects.get(
                category_name=data['category_name'])
        except:
            return Response({
                'message': 'category with this name is not exists..!!!',
                'status': status.HTTP_400_BAD_REQUEST
            })

        if category.is_delete == True:
            return Response({
                'message': 'category is already deleted',
                'status': status.HTTP_400_BAD_REQUEST
            })

        category.is_delete = True
        category.save()

        return Response({
            'message': 'category deleted',
            'status': status.HTTP_200_OK
        })


class CategoryMetaDataFieldView(APIView):

    def get(self, request):
        data = CategoryMetaDataField.objects.all()
        serializer = CategoryMetaDataFieldSerializer(data, many=True)
        return Response({
            'data': serializer.data,
            'status': status.HTTP_200_OK
        })

    def post(self, request):
        data = request.data
        serializer = CategoryMetaDataFieldSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response({
            'message': f'Field Saved',
            'status': status.HTTP_200_OK
        })


class CategoryMetaDataFieldValueView(APIView):

    def get(self, request):
        data = CategoryMetaDataFieldValue.objects.all()
        serializer = CategoryMetaDataFieldValueSerializer(data, many=True)

        return Response({
            'data': serializer.data,
            'status': status.HTTP_200_OK
        })

    def post(self, request):
        data = request.data
        serializer = CategoryMetaDataFieldValueSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response({
            'message': 'Data saved',
            'status': status.HTTP_200_OK
        })


class ProductView(APIView):

    def get(self, request):
        products = Product.objects.all()
        serialzier = ProductSerializer(products, many=True)

        return Response({
            'data': serialzier.data,
            'status': status.HTTP_200_OK
        })

    def post(self, reqeust):
        data = reqeust.data
        serializer = ProductSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({
            'message': 'product saved',
            'status': status.HTTP_200_OK,
            'data': serializer.data
        })


class ProductVariationView(APIView):

    def get(self, request):
        productvatiation = ProductVariation.objects.all()
        serializer = ProductVariationSerializer(productvatiation, many=True)

        return Response({
            'data': serializer.data,
            'status': status.HTTP_200_OK
        })

    def post(self, request):
        data = request.data
        serializer = ProductVariationSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({
            'message': 'product variation saved',
            'status': status.HTTP_200_OK,
            'data': serializer.data
        })


class ProductReviewView(APIView):

    def get(self, request):
        productreviews = ProductReview.objects.all()
        serializer = ProductReviewSerializer(productreviews, many=True)
        return Response({
            'data': serializer.data,
            'status': status.HTTP_200_OK
        })

    def post(self, request):
        data = request.data
        serializer = ProductReviewSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({
            'message': 'Review post',
            'status': status.HTTP_200_OK,
            'review': serializer.data
        })

    def delete(self, request):
        data = request.data
        review = ProductReview.objects.filter(
            customer=data['customer']).filter(product=data['product'])
        if not review:
            return Response({
                'message': 'review not found'
            })
        review.delete()
        return Response({
            'message': 'deleted'
        })


class CartView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        customer = Customer.objects.get(user=user)
        cart = Cart.objects.filter(customer=customer)
        serializer = CartSerializer(cart, many=True)
        return Response({
            'data': serializer.data,
            'status': status.HTTP_201_CREATED
        })

    def post(self, request):
        data = request.data
        user = request.user
        customer = Customer.objects.get(user=user)
        try:
            product_var = ProductVariation.objects.get(
                product=data['product_variation'])
        except:
            return Response({
                'message': 'product does not exist',
                'status': status.HTTP_400_BAD_REQUEST
            })
        try:
            cart = Cart.objects.filter(customer=customer).get(
                product_variation=data['product_variation'])
            if cart:
                cart.quantity = cart.quantity + 1
                cart.save()
        except:
            serializer = CartSerializer(data=data)
            if serializer.is_valid():
                Cart.objects.create(customer=customer, product_variation=product_var,
                                    quantity=serializer.data['quantity'], is_wishlist_item=serializer.data['is_wishlist_item'])

        return Response({
            'message': 'product added to cart',
            'status': status.HTTP_200_OK
        })


class OrderView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        customer = Customer.objects.get(user=user)
        orders = Order.objects.filter(customer=customer)
        serializer = OrderSerializer(orders, many=True)
        return Response({
            'orders': serializer.data,
            'status': status.HTTP_200_OK
        })

    def post(self, request):
        data = request.data
        user = request.user
        quantity = int(data['quantity'])
        try:
            customer = Customer.objects.get(user=user)
        except:
            return Response({
                'message': 'user not exist..!',
                'status': status.HTTP_400_BAD_REQUEST
            })

        try:
            product = ProductVariation.objects.get(
                product=data['product_variation'])
        except:
            return Response({
                'message': 'product not found!!',
                'status': status.HTTP_400_BAD_REQUEST
            })

        total_price = product.price * quantity

        serializer = OrderSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            order = Order.objects.create(
                customer=customer, amount_paid=total_price, **serializer.data)

            order_product = OrderProduct.objects.create(
                order=order, quantity=quantity, price=product.price, product_variation=product)

            orderstatus = OrderStatus.objects.create(
                order_product=order_product)

        return Response({
            'message': 'order placed',
            'status': status.HTTP_200_OK,
            'product': product.product.name,
            'quantity': quantity,
            'total_amount': total_price
        })
