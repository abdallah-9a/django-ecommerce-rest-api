from django.urls import path
from .views import CartView, AddItemView

urlpatterns = [
    path("cart/", CartView.as_view(), name="cart"),
    path("cart/add/", AddItemView.as_view(), name="add-item"),
]
