from django.db import models
from django.conf import settings
from products.models import Product

# Create your models here.


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default="pending")

    def __str__(self):
        return f"Order #{self.id} for {self.user.username} ({self.status})"

    def total_price(self):
        return sum(item.price * item.quantity for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_items"
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product} x {self.quantity} (order #{self.order.id})"

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.price

        return super().save(*args, **kwargs)
