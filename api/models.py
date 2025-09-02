from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

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

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            unique_slug = slug
            counter = 1
            while Category.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{slug}-{counter}"
                counter += 1

            self.slug = unique_slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
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

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            unique_slug = slug
            counter = 1
            while Product.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Cart(models.Model):
    cart_code = models.CharField(max_length=11, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cart_code
