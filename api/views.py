from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    CategoryDetailSerailizer,
    CategoryListSerializer,
)
from .models import Product, Category

# Create your views here.


@api_view(["GET"])
def product_list(requst):
    products = Product.objects.all()
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    serializer = ProductDetailSerializer(product)
    return Response(serializer.data)


@api_view(["GET"])
def category_list(request):
    category_list = Category.objects.all()
    serializer = CategoryListSerializer(category_list, many=True)
    return Response(serializer.data)
