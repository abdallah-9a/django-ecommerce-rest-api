from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import OrderSerializer, UpdateOrderStatusSerializer
from .models import Order, OrderItem
from common.pagination import CustomePagination

# Create your views here.


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomePagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["status"]

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
                    f"Not Enough Stock for {item.product}. Only {item.product.stock} left"
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


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class UpdateOrderStatusView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = UpdateOrderStatusSerializer
    permission_classes = [IsAdminUser]

    def perform_update(self, serializer):
        status = serializer.validated_data["status"]
        if status == "canceled":
            raise ValidationError("You can't cancel this order")
        return super().perform_update(serializer)


class CancelOrderView(generics.UpdateAPIView):
    serializer_class = UpdateOrderStatusSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        order = self.get_object()

        if order.user != request.user:
            raise ValidationError("You can only cancel your own orders")

        if order.status != "pending":
            raise ValidationError("Only pending order can be canceled")

        for item in order.items.all():
            item.product.stock += item.quantity
            item.product.save()

        order.status = "canceled"
        order.save()

        return Response(
            {"detail": "Your order has been canceled"}, status=status.HTTP_200_OK
        )
