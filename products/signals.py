from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings

import stripe

from .models import Product, Price

stripe.api_key = settings.STRIPE_SECRET_KEY


@receiver(post_save, sender=Product)
def create_or_update_stripe_product(sender, instance, created, **kwargs):
    if created or not instance.stripe_id:
        # Créer un produit sur Stripe
        stripe_product = stripe.Product.create(
            name=instance.name,
            description=instance.description,
            active=instance.active,
        )
        instance.stripe_id = stripe_product["id"]
        instance.save()
    else:
        # Mettre à jour le produit sur Stripe
        stripe.Product.modify(
            instance.stripe_id,
            name=instance.name,
            description=instance.description,
            active=instance.active,
        )


@receiver(post_save, sender=Price)
def create_or_update_stripe_price(sender, instance, created, **kwargs):
    if created or not instance.stripe_id:
        # Créer un prix sur Stripe
        stripe_price = stripe.Price.create(
            product=instance.product.stripe_id,
            unit_amount=int(instance.amount * 100),
            currency="eur",
            active=instance.active,
        )
        instance.stripe_id = stripe_price["id"]
        instance.save()
    else:
        # Mettre à jour le prix sur Stripe
        stripe.Price.modify(
            instance.stripe_id,
            unit_amount=int(instance.amount * 100),
            currency="eur",
            active=instance.active,
        )


@receiver(pre_save, sender=Product)
def deactivate_stripe_product(sender, instance, **kwargs):
    if not instance.active and instance.stripe_id:
        stripe.Product.modify(instance.stripe_id, active=False)


@receiver(pre_save, sender=Price)
def deactivate_stripe_price(sender, instance, **kwargs):
    if not instance.active and instance.stripe_id:
        stripe.Price.modify(instance.stripe_id, active=False)
