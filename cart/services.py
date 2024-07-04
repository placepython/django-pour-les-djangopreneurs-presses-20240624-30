from django.db.models import Sum
from django.conf import settings
from django.utils import timezone
from products.models import Price
from .models import CartItem

CART_SESSION_ID = getattr(settings, "CART_SESSION_ID", "cart")


class Cart:

    def __init__(self, request):
        self._session = request.session
        self._user = request.user
        self._cart = self._session.get(CART_SESSION_ID)
        if self._cart is None:
            self._cart = self._session[CART_SESSION_ID] = {}
        self.save()

    def save(self):
        self._session.modified = True

    def add(self, price, quantity=1):
        if self._user.is_authenticated:
            cart_item, created = CartItem.objects.get_or_create(
                user=self._user,
                price=price,
                defaults={
                    "quantity": quantity,
                },
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
        else:
            price_id = str(price.id)
            if price_id not in self._cart:
                self._cart[price_id] = {
                    "created": timezone.now().isoformat(),
                    "quantity": 0,
                }
            self._cart[price_id]["quantity"] += quantity
            self.save()

    def remove(self, price, quantity=1):
        if self._user.is_authenticated:
            item = CartItem.objects.filter(
                user=self._user, price=price
            ).first()
            if item:
                item.quantity -= quantity
                if item.quantity <= 0:
                    item.delete()
                else:
                    item.save()
        else:
            price_id = str(price.id)
            if price_id in self._cart:
                self._cart[price_id]["quantity"] -= quantity
                if self._cart[price_id]["quantity"] <= 0:
                    del self._cart[price_id]
                self.save()

    def __iter__(self):
        if self._user.is_authenticated:
            for item in CartItem.objects.filter(user=self._user):
                yield {
                    "price": item.price,
                    "quantity": item.quantity,
                    "created": item.created,
                }
        else:
            for price_id in self._cart:
                yield {
                    "price": Price.objects.get(id=price_id),
                    "quantity": int(self._cart[price_id]["quantity"]),
                    "created": timezone.datetime.fromisoformat(
                        self._cart[price_id]["created"]
                    ),
                }

    def __len__(self):
        if self._user.is_authenticated:
            total = CartItem.objects.filter(user=self._user).aggregate(
                total=Sum("quantity")
            )["total"]
            return total if total is not None else 0
        else:
            return sum(value["quantity"] for value in self._cart.values())

    def clear(self):
        if self._user.is_authenticated:
            CartItem.objects.filter(user=self._user).delete()
        else:
            self._session[CART_SESSION_ID] = {}
            self.save()
