from django.db import models
from django.conf import settings


class Product(models.Model):
    """Product sold by the application."""

    name = models.CharField("product name", max_length=255)
    description = models.TextField("product description", blank=True)
    stripe_id = models.CharField(
        "product stripe id", max_length=100, blank=True
    )
    images = models.ManyToManyField(
        "images.Image", through="ProductHasImage", related_name="products"
    )
    created = models.DateTimeField(
        "product creation date and time", auto_now_add=True
    )
    updated = models.DateTimeField(
        "product update date and time", auto_now=True
    )
    active = models.BooleanField("is product active ?", default=True)

    def __str__(self):
        return self.name


class ProductHasImage(models.Model):
    """Association between a product and its images."""

    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="product_images"
    )
    image = models.ForeignKey(
        "images.Image", on_delete=models.CASCADE, related_name="image_products"
    )
    created = models.DateTimeField(
        "product-image association date and time", auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("product", "image"),
                name="product_has_image_unique_relationship",
            )
        ]


class Price(models.Model):
    """Prices of a product."""

    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="prices"
    )
    description = models.TextField("price description", blank=True)
    stripe_id = models.CharField("price stripe id", max_length=150, blank=True)
    created = models.DateTimeField(
        "price creation date and time", auto_now_add=True
    )
    updated = models.DateTimeField("price update date and time", auto_now=True)
    active = models.BooleanField("is price active ?", default=True)
