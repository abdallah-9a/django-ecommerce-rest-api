from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from .models import Review, ProductRating


def update_product_rating(product): # need enhancement (optimization)
    reviews = product.reviews.all()
    total_reviews = reviews.count()

    reviews_avg = reviews.aggregate(Avg("rating"))["rating__avg"] or 0.0

    product_rating, created = ProductRating.objects.get_or_create(product=product)
    product_rating.avg_rating = reviews_avg
    product_rating.total_reviews = total_reviews
    product_rating.save()


@receiver(post_save, sender=Review)
def update_product_rating_on_save(sender, instance, **kwargs):
    update_product_rating(instance.product)


@receiver(post_delete, sender=Review)
def update_product_rating_on_delete(sender, instance, **kwargs):
    update_product_rating(instance.product)
