from django.db import models
from django.conf import settings
from products.models import Product

from django.core.exceptions import ValidationError

# Create your models here.


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart"
    )

    def __str__(self):
        return f"{self.user.username}'s Cart"

    def total(self):
        return sum(item.subtotal() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="items")
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("cart", "product")

    def __str__(self):
        return f"{self.product.name}"

    def clean(self):
        if self.quantity < 1:
            raise ValidationError("Quantity must be at least 1.")
        
        if self.quantity > self.product.stock:
            raise ValidationError(
                f"Only {self.product.stock} units available in stock."
            )

    def subtotal(self):
        return self.quantity * self.product.price
