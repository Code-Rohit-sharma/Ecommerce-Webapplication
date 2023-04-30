from django.urls import path
from . import views

urlpatterns = [
    path('parentcategory/',views.ParentCategoryView.as_view(),name='parent_category'),
    path('category/',views.CategoryView.as_view(),name='category'),
    path('category-metadata-field/',views.CategoryMetaDataFieldView.as_view(),name='category-metadata-field'),
    path('category-metadata-field-value/',views.CategoryMetaDataFieldValueView.as_view(),name='category-metadata-field-value'),
    path('products/',views.ProductView.as_view(),name='category'),
    path('product-variation/',views.ProductVariationView.as_view(),name='product-variation'),
]