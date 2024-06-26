from django.db import models

from django.conf import settings


class Article(models.Model):
    title = models.CharField("article title", max_length=255)
    content = models.TextField("article content", blank=True)
    pub_date = models.DateTimeField(
        "article publication date", blank=True, null=True
    )
    creation_date = models.DateTimeField(
        "article creation date", auto_now_add=True
    )
    update_date = models.DateTimeField("article update date", auto_now=True)
    active = models.BooleanField("is article active ?", default=False)
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="articles",
    )
    tags = models.ManyToManyField("Tag", related_name="articles")

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField("tag name", max_length=50)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField("category name", max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"


class Comment(models.Model):
    content = models.TextField("comment content")
    article = models.ForeignKey(
        "Article", on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        "Author", on_delete=models.CASCADE, related_name="comments"
    )

    def __str__(self):
        return self.content


class Author(models.Model):
    email = models.EmailField("author email", unique=True)

    def __str__(self):
        return self.email
