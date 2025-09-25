from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from .models import CartItem
from users.models import User
from products.models import Product, Category


class CartAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.cart_url = reverse("cart")
        self.add_item_url = reverse("add-item")
        self.user = User.objects.create_user(
            username="username", email="user@gmail.com", password="UserName"
        )
        self.category = Category.objects.create(name="Books")
        self.product = Product.objects.create(
            name="Cook Book", price=100, category=self.category, stock=10
        )

    def authenticate(self):
        self.client.force_authenticate(self.user)

    def test_cart_access(self):
        # Unauthenticated access
        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authenticated access
        self.authenticate()
        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_item_to_cart(self):
        data = {"product": self.product.slug, "quantity": 2}

        # Unauthenticated add
        response = self.client.post(self.add_item_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authenticated add
        self.authenticate()
        response = self.client.post(self.add_item_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            CartItem.objects.filter(product=self.product, cart=self.user.cart).exists()
        )

    def test_update_quantity(self):
        quantity_data = {"quantity": 10}

        # Add item to cart to get its pk
        self.authenticate()
        add_response = self.client.post(
            self.add_item_url, {"product": self.product.slug, "quantity": 2}
        )
        cart_item_id = CartItem.objects.get(
            cart=self.user.cart, product=self.product
        ).pk
        update_url = reverse("update-quantity", kwargs={"pk": cart_item_id})

        # Unauthenticated update
        self.client.force_authenticate(user=None)
        response = self.client.patch(update_url, quantity_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authenticated update
        self.authenticate()
        response = self.client.patch(update_url, quantity_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CartItem.objects.get(pk=cart_item_id).quantity, 10)

    def test_update_quantity_not_found(self):
        self.authenticate()
        update_url = reverse("update-quantity", kwargs={"pk": 9999})
        response = self.client.patch(update_url, {"quantity": 5})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
