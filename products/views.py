from django.shortcuts import render
from rest_framework import generics
from .models import Product, Category
from .serializers import ProductListSerializer, CategorySerializer
from common.pagination import CustomePagination
from common.permissions import IsAdminOrReadOnly

# Create your views here.


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = CustomePagination


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CustomePagination
    permission_classes = [IsAdminOrReadOnly]
