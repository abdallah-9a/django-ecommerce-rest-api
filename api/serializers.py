from rest_framework import serializers
from .models import Product, Category, Cart, CartItem, Review, Wishlist
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "first_name", "last_name", "email", "profile_picture_url"]


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


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ["id", "user", "rating", "review", "created_at", "updated_at"]


class WishlistSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    products = ProductListSerializer(read_only=True, many=True)

    class Meta:
        model = Wishlist
        fields = ["id", "user", "products", "created_at"]
