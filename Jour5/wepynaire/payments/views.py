from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from guardian.shortcuts import assign_perm
import stripe

from wepynaire.products.models import Price
from wepynaire.payments.models import Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(LoginRequiredMixin, View):
    def post(self, request, price_id):
        """Creates a stripe checkout session and redirects the user to stripe
        website."""
        price = get_object_or_404(Price, id=price_id)
        order = Order.objects.create(user=request.user)
        OrderItem.objects.create(order=order, unit_price=price)
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        "price": price.stripe_id,
                        "quantity": 1,
                    },
                ],
                client_reference_id=order.id,
                mode="payment",
                success_url="http://localhost:8000/payments/success/",
                cancel_url="http://localhost:8000/payments/cancel/",
            )
        except Exception as e:
            return str(e)

        return redirect(checkout_session.url)


@csrf_exempt
@require_POST
def stripe_webhook(request):
    """Receives and process stripe events."""
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET_KEY
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
        session = stripe.checkout.Session.retrieve(
            event["data"]["object"]["id"],
            expand=["line_items"],
        )

        process_order_after_payment_success(event, session)

    # Passed signature verification
    return HttpResponse(status=200)


def process_order_after_payment_success(event, session):
    """Process an order after payment has been confirmed by stripe."""
    # Retrieve the order from its client reference id
    order_id = int(session["client_reference_id"])
    order = Order.objects.get(id=order_id)

    # Extract useful payment info from the stripe checkout sessiojn
    customer_email = session["customer_details"]["email"]
    payment_intent = session["payment_intent"]

    # Update order object to make it paid and store the ref of the stripe
    # transaction
    order.is_paid = True
    order.stripe_intent_id = payment_intent
    order.stripe_customer_email = customer_email
    order.save()

    # Affectation des permission
    price = order.items.first()
    assign_perm("products.view_product", order.user, price.product)
    if "version video" in price.description.lower():
        assign_perm("products.access_video", order.user, price.product)
