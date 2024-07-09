from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "payments"

urlpatterns = [
    path(
        "<int:price_id>/",
        views.CreateCheckoutSessionView.as_view(),
        name="create-checkout-session",
    ),
    path(
        "success/",
        TemplateView.as_view(template_name="payments/success.html"),
        name="success",
    ),
    path(
        "cancel/",
        TemplateView.as_view(template_name="payments/cancel.html"),
        name="cancel",
    ),
    path("webhook/", views.stripe_webhook, name="stripe-webhook"),
]
