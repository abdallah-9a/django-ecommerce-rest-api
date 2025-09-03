from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    CategoryDetailSerailizer,
    CategoryListSerializer,
    CartSerializer,
    CartItemSerializer,
    ReviewSerializer,
    WishlistSerializer,
)
from .models import Product, Category, Cart, CartItem, Review, Wishlist

User = get_user_model()
# Create your views here.


@api_view(["GET"])
def product_list(requst):
    products = Product.objects.all()
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    serializer = ProductDetailSerializer(product)
    return Response(serializer.data)


@api_view(["GET"])
def category_list(request):
    category_list = Category.objects.all()
    serializer = CategoryListSerializer(category_list, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def category_detail(request, slug):
    category = Category.objects.get(slug=slug)
    serializer = CategoryDetailSerailizer(category)
    return Response(serializer.data)


# @api_view(["POST"])
# def add_to_cart(request):
#     cart_code = request.data.get("cart_code")
#     product_id = request.data.get("product_id")

#     cart, created = Cart.objects.get_or_create(cart_code=cart_code)
#     product = Product.objects.get(id=product_id)

#     cartitem, created = CartItem.objects.get_or_create(product=product, cart=cart)
#     cartitem.quantity = 1
#     cartitem.save()

#     serializer = CartSerializer(cart)
#     return Response(serializer.data)


@api_view(["PUT"])
def update_cart_quantity(request, item_id):
    quantity = request.data.get("quantity")
    quantity = int(quantity)

    item = CartItem.objects.get(id=item_id)
    item.quantity = quantity
    item.save()

    serializer = CartItemSerializer(item)
    return Response(serializer.data)


# @api_view(["GET"])
# def cart_detail(request):
#     cart_code = request.query_params.get("cart_code")
#     cart = Cart.objects.get(cart_code=cart_code)

#     serializer = CartSerializer(cart)
#     return Response(serializer.data)


@api_view(["GET", "POST"])
def cart_view(request):
    method = request.method
    if method == "POST":  # add product to cart
        cart_code = request.data.get("cart_code")
        product_id = request.data.get("product_id")

        cart, created = Cart.objects.get_or_create(cart_code=cart_code)
        product = Product.objects.get(id=product_id)

        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        item.quantity = 1
        item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data)

    if method == "GET":  # get cart detail
        cart_code = request.query_params.get("cart_code")
        cart = Cart.objects.get(cart_code=cart_code)

        serializer = CartSerializer(cart)
        return Response(serializer.data)


@api_view(["GET", "POST", "PUT", "DELETE"])
def review_view(request, product_id, review_id=None):
    method = request.method
    if method == "GET":
        product = Product.objects.get(id=product_id)
        reviews = product.reviews

        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    elif method == "POST":
        email = request.data.get("email")
        msg = request.data.get("review")
        rating = request.data.get("rating")

        product = Product.objects.get(id=product_id)
        user = User.objects.get(email=email)

        if Review.objects.filter(product=product, user=user).exists():
            return Response(
                "You are already dropped a review for this product", status=400
            )

        review = Review.objects.create(
            product=product, user=user, rating=rating, review=msg
        )

        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    elif method == "PUT":
        review = Review.objects.get(id=review_id)
        msg = request.data.get("review")
        rating = request.data.get("rating")

        review.review = msg
        review.rating = rating
        review.save()

        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    elif method == "DELETE":
        review = Review.objects.get(id=review_id)
        review.delete()

        return Response("Review deleted Successfully", status=204)


@api_view(["GET", "POST", "DELETE"])
def wishlist_view(request, product_id=None):
    method = request.method
    if method == "GET":
        email = request.query_params.get("email")
        user = User.objects.get(email=email)
        wishlist, _ = Wishlist.objects.get_or_create(user=user)

        serializer = WishlistSerializer(wishlist)

        return Response(serializer.data)

    elif method == "POST":
        email = request.data.get("email")
        user = User.objects.get(email=email)
        wishlist, _ = Wishlist.objects.get_or_create(user=user)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product Not Found"}, status=404)

        wishlist.products.add(product)

        serializer = WishlistSerializer(wishlist)

        return Response(serializer.data)

    elif method == "DELETE":
        email = request.data.get("email")
        user = User.objects.get(email=email)
        product = Product.objects.get(id=product_id)
        wishlist = Wishlist.objects.get(user=user)

        wishlist.products.remove(product)

        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)
