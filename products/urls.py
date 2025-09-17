from django.urls import path
from .views import (
    ProductListCreateView,
    ProductView,
    CategoryListCreateView,
    CategoryView,
)

urlpatterns = [
    path("products/", ProductListCreateView.as_view(), name="products"),
    path("products/<int:pk>/", ProductView.as_view(), name="product-detail"),
    path("categories/", CategoryListCreateView.as_view(), name="categories"),
    path("categories/<int:pk>/", CategoryView.as_view(), name="category-detail"),
]
