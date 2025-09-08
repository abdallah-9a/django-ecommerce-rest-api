import stripe
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import authentication, permissions
from django.db.models import Q
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
from .models import (
    Product,
    Category,
    Cart,
    CartItem,
    Review,
    Wishlist,
    Order,
    OrderItem,
)

User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.WEBHOOK_SECRET
# Create your views here.


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    authentication_classes = [
        authentication.BasicAuthentication
    ]  # isn't important in this case, but add anyway
    permission_classes = [permissions.AllowAny]


@api_view(["GET"])
def product_list(requst):
    products = Product.objects.all()
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"


@api_view(["GET"])
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    serializer = ProductDetailSerializer(product)
    return Response(serializer.data)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.AllowAny]


@api_view(["GET"])
def category_list(request):
    category_list = Category.objects.all()
    serializer = CategoryListSerializer(category_list, many=True)
    return Response(serializer.data)


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerailizer
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"


@api_view(["GET"])
def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    serializer = CategoryDetailSerailizer(category)
    return Response(serializer.data)


class CartView(generics.GenericAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart

    def get(self, request, *args, **kwargs):
        cart = self.get_object(request)

        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """Add new product, or update quantity for a product"""
        cart = self.get_object(request)
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))  # Default = 1

        product = get_object_or_404(Product, id=product_id)

        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if quantity <= 0:
            return Response({"error": "Quantity Must be positive"}, status=400)
        item.quantity = quantity

        item.save()

        serailizer = self.get_serializer(cart)
        return Response(serailizer.data)

    def delete(self, request, *args, **kwargs):
        cart = self.get_object(request)
        product_id = request.data.get("product_id")

        if not product_id:
            return Response({"error": "Product Id is required"}, status=400)

        product = get_object_or_404(Product, id=product_id)

        try:
            item = get_object_or_404(CartItem, cart=cart, product=product)
            item.delete()
            return Response({"message": "Product removed from cart"})

        except CartItem.DoesNotExist:
            return Response({"error": "Product not found in cart"})


@api_view(["GET", "POST", "DELETE"])
def cart_view(request, product_id=None):
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

    elif method == "GET":  # get cart detail
        cart_code = request.query_params.get("cart_code")
        cart = get_object_or_404(Cart, cart_code=cart_code)

        serializer = CartSerializer(cart)
        return Response(serializer.data)
    elif method == "DELETE":
        cart_code = request.data.get("cart_code")
        try:
            cart = get_object_or_404(Cart, cart_code=cart_code)
        except Cart.DoesNotExist:
            return Response("Cart Doesn't Exist", status=404)
        try:
            product = get_object_or_404(Product, id=product_id)
        except Product.DoesNotExist:
            return Response("Product Doesn't Exist", status=404)
        try:
            item = get_object_or_404(CartItem, cart=cart, product=product)
            item.delete()
        except CartItem.DoesNotExist:
            return Response("Item Doesn't Exists", status=404)

        return Response("Product Deleted Successfully")


@api_view(["GET", "POST", "PUT", "DELETE"])
def review_view(request, product_id, review_id=None):
    method = request.method
    if method == "GET":
        product = get_object_or_404(Product, id=product_id)
        reviews = product.reviews

        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    elif method == "POST":
        email = request.data.get("email")
        msg = request.data.get("review")
        rating = request.data.get("rating")

        product = get_object_or_404(Product, id=product_id)
        user = get_object_or_404(User, email=email)

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
        review = get_object_or_404(Review, id=review_id)
        review.delete()

        return Response("Review deleted Successfully", status=204)


@api_view(["GET", "POST", "DELETE"])
def wishlist_view(request, product_id=None):
    method = request.method
    if method == "GET":
        email = request.query_params.get("email")
        user = get_object_or_404(User, email=email)
        wishlist, _ = Wishlist.objects.get_or_create(user=user)

        serializer = WishlistSerializer(wishlist)

        return Response(serializer.data)

    elif method == "POST":
        email = request.data.get("email")
        user = get_object_or_404(User, email=email)
        wishlist, _ = Wishlist.objects.get_or_create(user=user)

        try:
            product = get_object_or_404(Product, id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product Not Found"}, status=404)

        wishlist.products.add(product)

        serializer = WishlistSerializer(wishlist)

        return Response(serializer.data)

    elif method == "DELETE":
        email = request.data.get("email")
        user = get_object_or_404(User, email=email)
        product = get_object_or_404(Product, id=product_id)
        wishlist = get_object_or_404(Wishlist, user=user)

        wishlist.products.remove(product)

        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)


@api_view(["GET"])
def product_search(request):
    query = request.query_params.get("q", "")
    if not query:
        return Response({"error": "No search query provided"}, status=400)

    products = Product.objects.filter(
        Q(name__icontains=query)
        | Q(description__icontains=query)
        | Q(category__name__icontains=query)
    )

    if not products.exists():
        return Response({"message": "No products found"})

    serializer = ProductListSerializer(products, many=True)

    return Response(serializer.data)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


@api_view(["POST"])
def create_checkout_session(request):
    cart_code = request.data.get("cart_code")
    email = request.data.get("email")
    cart = get_object_or_404(Cart, cart_code=cart_code)

    try:
        checkout_session = stripe.checkout.Session.create(
            customer_email=email,
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": item.product.name},
                        "unit_amount": int(item.product.price * 100),  # amount in cents
                    },
                    "quantity": item.quantity,
                }
                for item in cart.cart_items.all()
            ],
            mode="payment",
            success_url="http://localhost:8000/api/payment/success/",
            cancel_url="http://localhost:8000/api/payment/cancel/",
            metadata={"cart_code": cart_code},
        )

        return Response({"checkout_url": checkout_session.url})

    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(["GET"])
def payment_success(request):
    return Response({"status": "success", "message": "Payment Completed!"})


@api_view(["GET"])
def payment_cancel(request):
    return Response({"status": "cancelled", "message": "Payment was calcelled!"})


@csrf_exempt
def webhook_view(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if (
        event["type"] == "checkout.session.completed"
        or event["type"] == "checkout.session.async_payment_succeeded"
    ):
        session = event["data"]["object"]
        cart_code = session.get("metadata", {}).get("cart_code")
        fulfill_checkout(session, cart_code)

    return HttpResponse(status=200)


def fulfill_checkout(session, cart_code):
    order, created = Order.objects.get_or_create(
        stripe_checkout_id=session["id"],
        defaults={
            "amount": session["amount_total"] / 100,
            "currency": session["currency"],
            "customer_email": session["customer_email"],
            "status": "Paid",
        },
    )

    if created and cart_code:
        cart = get_object_or_404(Cart, cart_code=cart_code)
        for item in cart.cart_items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
            )
