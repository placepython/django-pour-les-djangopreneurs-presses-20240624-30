from django.shortcuts import render, get_object_or_404

from .models import Product


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(
        request, "products/detail.html", context={"product": product}
    )
