from django.urls import reverse, resolve
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from products.models import Product, Category
from users.models import User

# Create your tests here.


class ProductListCreateAPITestCase(APITestCase):
    def setUp(self):
        self.url = reverse("products")
        self.category = Category.objects.create(name="electronics")
        self.product = Product.objects.create(
            name="phone", price=1000, category=self.category
        )
        self.client = APIClient()
        self.adminuser = User.objects.create_superuser(
            email="admin@gmail.com", password="AdminUser", username="AdminUser"
        )
        self.user = User.objects.create_user(
            email="user@gmail.com", password="NormalUser", username="NormalUser"
        )

    def test_products_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "phone")

    def test_create_product(self):
        data = {"name": "Laptop", "price": 10000, "category": self.category}

        # Unauthenticated user
        anon_client = APIClient()
        response = anon_client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Normal user should not be allowed to create a product
        normal_client = APIClient()
        normal_client.force_authenticate(user=self.user)
        response = normal_client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Admin user should be able to create a product successfully
        admin_client = APIClient()
        admin_client.force_authenticate(user=self.adminuser)
        response = admin_client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Product.objects.filter(name="Laptop").exists())


class ProductDetailAPITestCase(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="electronics")
        self.product = Product.objects.create(
            name="phone", price=1000, category=self.category
        )
        self.client = APIClient()
        self.url = reverse("product-detail", kwargs={"pk": self.product.pk})
        self.adminuser = User.objects.create_superuser(
            email="admin@gmail.com", password="AdminUser", username="AdminUser"
        )
        self.user = User.objects.create_user(
            email="user@gmail.com", password="NormalUser", username="NormalUser"
        )

    def test_retrieve_product(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "phone")

    def test_update_product(self):
        data = {"name": "IPhone 4", "price": 1200, "category": self.category}

        # Unauthenticated
        anon_client = APIClient()
        response = anon_client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Normal User
        normal_client = APIClient()
        normal_client.force_authenticate(user=self.user)
        response = normal_client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Admin User
        admin_client = APIClient()
        admin_client.force_authenticate(user=self.adminuser)
        response = admin_client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Product.objects.filter(name="IPhone 4").exists())

    def test_delete_product(self):
        # Unauthenticated
        anon_client = APIClient()
        response = anon_client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Normal User
        normal_client = APIClient()
        normal_client.force_authenticate(user=self.user)
        response = normal_client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Admin User
        admin_client = APIClient()
        admin_client.force_authenticate(user=self.adminuser)
        response = admin_client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())


class CategoryListCreateAPITestCase(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.client = APIClient()
        self.url = reverse("categories")
        self.adminuser = User.objects.create_superuser(
            email="admin@gmail.com", password="AdminUser", username="AdminUser"
        )
        self.user = User.objects.create_user(
            email="user@gmail.com", password="NormalUser", username="NormalUser"
        )

    def test_categories_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Electronics")

    def test_create_category(self):
        data = {"name": "Books"}

        # UnAuthenticated
        anon_client = APIClient()
        response = anon_client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Normal User
        normal_client = APIClient()
        normal_client.force_authenticate(self.user)
        response = normal_client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Admin USer
        admin_client = APIClient()
        admin_client.force_authenticate(self.adminuser)
        response = admin_client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Category.objects.filter(name="Books").exists())


class CategoryDetailAPITestCase(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.client = APIClient()
        self.url = reverse("category-detail", kwargs={"pk": self.category.pk})
        self.adminuser = User.objects.create_superuser(
            email="admin@gmail.com", password="AdminUser", username="AdminUser"
        )
        self.user = User.objects.create_user(
            email="user@gmail.com", password="NormalUser", username="NormalUser"
        )

    def test_retrieve_category(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_category(self):
        data = {"name": "Books"}

        # UnAthenticated
        anon_client = APIClient()
        response = anon_client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Normal User
        normal_client = APIClient()
        normal_client.force_authenticate(self.user)
        response = normal_client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Admin User
        admin_client = APIClient()
        admin_client.force_authenticate(self.adminuser)
        response = admin_client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Category.objects.filter(name="Books").exists())

    def test_delete_category(self):

        # UnAthenticated
        anon_client = APIClient()
        response = anon_client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Normal User
        normal_client = APIClient()
        normal_client.force_authenticate(self.user)
        response = normal_client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Admin User
        admin_client = APIClient()
        admin_client.force_authenticate(self.adminuser)
        response = admin_client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(name="Books").exists())
