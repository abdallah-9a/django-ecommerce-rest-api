from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.product_list, name="product_list"),
    path("products/<slug:slug>/", views.product_detail, name="product_detail"),
    path("categories/", views.category_list, name="category_list"),
    path("categories/<slug:slug>/", views.category_detail, name="category_detail"),
    path("cart/", views.cart_view, name="add_to_cart"),  # POST
    path("cart/", views.cart_view, name="view_cart"),  # GET
    path(
        "cart/<int:item_id>/",
        views.update_cart_quantity,
        name="update_cart_quantity",  # PUT
    ),
    path("products/<int:id>/reviews/", views.review_view, name="Add_review"),  # POST
    path("products/<int:id>/reviews/", views.review_view, name="reviews_list"),  # GET
]
