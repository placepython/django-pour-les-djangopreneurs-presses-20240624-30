from django.db import models
from django.conf import settings


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
    )
    is_paid = models.BooleanField("is order paid ?", default=False)
    stripe_customer_email = models.EmailField(
        "order stripe customer email", blank=True
    )
    stripe_intent_id = models.CharField(
        "order stripe intent id", max_length=255, blank=True
    )
    created = models.DateTimeField(
        "order creation date and time", auto_now_add=True
    )
    updated = models.DateTimeField("order update date and time", auto_now=True)

    def __str__(self):
        return f"Commande de {self.user.email} du {self.created.strftime('%d/%m/%Y à %Hh:%M:%S')}: {'payé' if self.is_paid else 'non payé'}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        "Order", on_delete=models.CASCADE, related_name="items"
    )
    unit_price = models.ForeignKey(
        "products.Price",
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(
        "item quantity", blank=True, default=1
    )
    created = models.DateTimeField(
        "item creation date and time", auto_now_add=True
    )
    updated = models.DateTimeField("item update date and time", auto_now=True)

    def __str__(self):
        return f"Commande de {self.order.user.email} du {self.order.created.strftime('%d/%m/%Y à %Hh:%M:%S')}: {self.quantity} x {self.unit_price} ({self.unit_price.price} CHF)"
