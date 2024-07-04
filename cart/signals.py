from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone

from .models import CartItem
from products.models import Price

CART_SESSION_ID = getattr(settings, "CART_SESSION_ID", "cart")


@receiver(user_logged_in)
def merge_carts(sender, request, user, **kwargs):
    session_cart = request.session.get(CART_SESSION_ID, {})

    for price_id, item in session_cart.items():
        price = Price.objects.get(id=int(price_id))
        cart_item, created = CartItem.objects.get_or_create(
            user=user,
            price=price,
            defaults={
                "quantity": item["quantity"],
                "created": timezone.datetime.fromisoformat(item["created"]),
            },
        )
        if not created:
            cart_item.quantity += item["quantity"]
            cart_item.save()

    request.session[CART_SESSION_ID] = {}
    request.session.modified = True
