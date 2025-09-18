from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ValidationError
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import CartSerializer, CartItemSerializer, CartItemUpdateSerializer
from .models import Cart, CartItem

# Create your views here.


class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Cart, user=self.request.user)


class AddItemView(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        cart = self.request.user.cart
        product = serializer.validated_data["product"]
        if CartItem.objects.filter(cart=cart, product=product).exists():
            raise ValidationError(
                {"error": "Product already in cart. Use the update endpoint instead"}
            )

        serializer.save(cart=cart)


class UpdateQuantityView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    def perform_update(self, serializer):
        quantity = serializer.validated_data["quantity"]
        serializer.save(quantity=quantity)
        
    
