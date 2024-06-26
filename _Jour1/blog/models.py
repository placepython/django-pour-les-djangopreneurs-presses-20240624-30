from django.db import models


class Article(models.Model):
    title = models.CharField("article title", max_length=255)
    content = models.TextField("article content", blank=True)
    pub_date = models.DateTimeField("article publication date", blank=True)
    creation_date = models.DateTimeField(
        "article creation date", auto_now_add=True
    )
    update_date = models.DateTimeField("article update date", auto_now=True)
    active = models.BooleanField("is article active ?", default=False)
    category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, blank=True, null=True
    )


class Category(models.Model):
    name = models.CharField("category name", max_length=50)
