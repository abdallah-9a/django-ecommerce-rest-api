from rest_framework import serializers
from .models import Product, Category, Cart, CartItem


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "slug", "image", "price"]


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "description", "slug", "image", "price"]


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "image", "slug"]


class CategoryDetailSerailizer(serializers.ModelSerializer):
    products = ProductListSerializer(read_only=True, many=True)

    class Meta:
        model = Category
        fields = ["id", "name", "image", "products"]


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    sub_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "sub_total"]

    def get_sub_total(self, cartitem):
        total = cartitem.quantity * cartitem.product.price
        return total


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(read_only=True, many=True)
    cart_total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "cart_code", "cart_items", "cart_total"]

    def get_cart_total(self, cart):
        items = cart.cart_items.all()
        total = sum([item.product.price * item.quantity for item in items])
        return total
