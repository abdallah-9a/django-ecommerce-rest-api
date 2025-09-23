from django.test import TestCase
from .models import Product, Category

# Create your tests here.


class ModelsTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name="name")
        self.product = Product.objects.create(
            name="Café C++ Primer #1 — Version 2.0_beta-ALPHA@Email/Path&Rock, Roll!!!",  # cover almost all cases
            price=100,
            category=category,
        )

    def test_product_model_slug(self):
        self.assertEqual(
            self.product.slug,
            "cafe-c++-primer-#1-version-2.0_beta-alpha-email-path-rock-roll",
        )
