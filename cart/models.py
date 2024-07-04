from django.db import models
from django.conf import settings


class CartItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="user",
        on_delete=models.CASCADE,
        related_name="cart_items",
    )
    price = models.ForeignKey(
        "products.Price",
        verbose_name="price",
        on_delete=models.CASCADE,
        related_name="cart_items",
    )
    quantity = models.PositiveIntegerField(
        "item quantity",
        default=1,
    )
    created = models.DateTimeField(
        "item creation date and time",
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        "item update date and time",
        auto_now=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("user", "price"),
                name="user_price_unique_constraint",
            )
        ]
