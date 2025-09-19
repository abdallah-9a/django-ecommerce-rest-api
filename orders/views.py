from django.shortcuts import render
from django.core.exceptions import ValidationError
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderSerializer, OrderItemSerializer
from .models import Order, OrderItem
from cart.models import Cart

# Create your views here.


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        cart = self.request.user.cart
        if not cart.items.exists():
            raise ValidationError("Your Cart is Empty")

        order = serializer.save(user=self.request.user)

        for item in cart.items.all():
            if item.quantity > item.product.stock:
                raise ValidationError(
                    "Not Enough Stock for {item.product}. Only {item.product.stock} left"
                )
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity,
            )

            item.product.stock -= item.quantity
            item.product.save()

            cart.items.all().delete()
