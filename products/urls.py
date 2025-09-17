from django.urls import path
from .views import ProductListCreateView, CategoryListCreateView

urlpatterns = [
    path("products/", ProductListCreateView.as_view(), name="products"),
    path("categories/", CategoryListCreateView.as_view(), name="categories"),
]
