from django import forms
from django.core.exceptions import ValidationError

from blog.models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ("title", "content", "pub_date")

    def clean_title(self):
        title = self.cleaned_data.get("title")

        if title != title.lower():
            raise ValidationError(
                "le titre de l'article ne doit contenir que des minuscules"
            )

        return title

    def clean_content(self):
        return self.cleaned_data.get("content")
