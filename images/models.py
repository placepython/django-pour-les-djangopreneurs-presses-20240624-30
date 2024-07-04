from django.db import models


class Image(models.Model):
    image = models.ImageField(upload_to="images/%Y/%m/%d")
    alt_text = models.CharField(
        "image alt text",
        max_length=255,
        blank=True,
    )
    title = models.CharField(
        "image title",
        max_length=255,
        blank=True,
    )
    created = models.DateTimeField(
        "image creation date and time", auto_now_add=True
    )
    updated = models.DateTimeField(
        "image update date and time",
        auto_now=True,
    )
