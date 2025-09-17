from django.shortcuts import render
from rest_framework import generics
from .models import Product, Category
from .serializers import (
    ProductListSerializer,
    ProductSerializer,
    CategorySerializer,
    CategoryListSerializer,
)
from common.pagination import CustomePagination
from common.permissions import IsAdminOrReadOnly

# Create your views here.


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = CustomePagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProductListSerializer

        return ProductSerializer


class ProductView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    pagination_class = CustomePagination
    permission_classes = [IsAdminOrReadOnly]


class CategoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
