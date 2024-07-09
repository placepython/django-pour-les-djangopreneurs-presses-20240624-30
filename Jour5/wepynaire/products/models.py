from django.db import models
from django.conf import settings


class Product(models.Model):
    name = models.CharField("product name", max_length=255)
    description = models.TextField("product description", blank=True)
    stripe_id = models.CharField(
        "product stripe id", max_length=100, blank=True
    )
    active = models.BooleanField("is product active ?", default=True)
    clients = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="products"
    )

    class Meta:
        permissions = (("access_video", "can read texts and videos"),)

    def __str__(self):
        return self.name


class Price(models.Model):
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="prices"
    )
    description = models.CharField(
        "price description", max_length=255, blank=True
    )
    stripe_id = models.CharField("price stripe id", max_length=100, blank=True)
    active = models.BooleanField("is price active ?", default=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.description}"
