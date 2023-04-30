from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import ParentCategorySerializer, CategorySerializer, CategoryMetaDataFieldSerializer, CategoryMetaDataFieldValueSerializer, ProductSerializer, ProductVariationSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import ParentCategory, Category, CategoryMetaDataField, CategoryMetaDataFieldValue, Product, ProductVariation
from rest_framework.permissions import AllowAny

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

        if serializer.is_valid():
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
        if serializer.is_valid():
            serializer.save()
        return Response({
            'message': 'product saved',
            'status': status.HTTP_200_OK
        })


class ProductVariationView(APIView):

    def get(self, request):
        productvatiation = ProductVariation.objects.all()
        serializer = ProductVariationSerializer(productvatiation, many=True)

        return Response({
            'data': serializer.data,
            'status': status.HTTP_200_OK
        })
