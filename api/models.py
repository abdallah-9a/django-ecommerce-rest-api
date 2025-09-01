from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to="categories_img", blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    desciption = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to="products_img", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="products",
    )

    def __str__(self):
        return self.name
