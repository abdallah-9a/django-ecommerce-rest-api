from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product
from products.serializers import ProductListSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "subtotal"]

    def get_subtotal(self, obj):
        return obj.subtotal()


class CartItemCreateSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(
        queryset=Product.objects.all(), slug_field="slug"
    )

    class Meta:
        model = CartItem
        fields = ["product", "quantity"]

    def validate(self, attrs):
        product = attrs.get("product")
        quantity = attrs.get("quantity")

        if quantity <= 0:
            raise ValidationError("Quantity must be at least 1")

        if quantity > product.stock:
            raise ValidationError(f"Only {product.stock} units available in stock")

        return attrs


class CartSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "user", "items", "total"]

    def get_total(self, obj):
        return obj.total()
