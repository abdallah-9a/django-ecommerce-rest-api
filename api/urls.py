from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.product_list, name="product_list"),
    path("products/search/", views.product_search, name="product_search"),
    path("products/<slug:slug>/", views.product_detail, name="product_detail"),
    path("categories/", views.category_list, name="category_list"),
    path("categories/<slug:slug>/", views.category_detail, name="category_detail"),
    path("cart/add/<int:product_id>/", views.cart_view, name="add_to_cart"),  # POST
    path(
        "cart/delete/<int:product_id>/", views.cart_view, name="remove_from_cart"
    ),  # DELETE
    path("cart/", views.cart_view, name="view_cart"),  # GET
    path(
        "cart/<int:item_id>/",
        views.update_cart_quantity,
        name="update_cart_quantity",  # PUT
    ),
    path("products/<int:id>/reviews/", views.review_view, name="Add_review"),  # POST
    path("products/<int:id>/reviews/", views.review_view, name="reviews_list"),  # GET
    path(
        "products/<int:product_id>/reviews/<int:review_id>/",
        views.review_view,
        name="update_review",
    ),  # PUT
    path(
        "products/<int:product_id>/reviews/<int:review_id>/",
        views.review_view,
        name="delete_review",
    ),  # DELETE
    path(
        "wishlist/add/<int:product_id>/", views.wishlist_view, name="add_to_wishlist"
    ),  # POST
    path(
        "wishlist/add/<int:product_id>/",
        views.wishlist_view,
        name="delete_from_wishlist",
    ),  # DELETE
    path("wishlist/", views.wishlist_view, name="wishlist_items"),  # GET
    path(
        "checkout/create/", views.create_checkout_session, name="create_checkout"
    ),  # POST
    path("payment/success/", views.payment_success, name="payment_success"),  # GET
    path("payment/cancel/", views.payment_cancel, name="payment_cancelled"),  # GET
]
