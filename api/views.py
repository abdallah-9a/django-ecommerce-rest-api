from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    CategoryDetailSerailizer,
    CategoryListSerializer,
    CartSerializer,
    CartItemSerializer,
)
from .models import Product, Category, Cart, CartItem

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
