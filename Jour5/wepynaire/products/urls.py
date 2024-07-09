from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("<int:product_id>/", views.product_detail, name="detail"),
]
