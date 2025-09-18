from django.urls import path
from .views import CartView, AddItemView, UpdateQuantityView

urlpatterns = [
    path("cart/", CartView.as_view(), name="cart"),
    path("cart/add/", AddItemView.as_view(), name="add-item"),
    path("cart/items/<int:pk>/", UpdateQuantityView.as_view(), name="update-quantity"),
]
