from django.shortcuts import render, redirect
from django.views.generic import View

from wepynaire.blog.forms import ArticleForm


def hx_affichage(request):
    return render(request, "pages/affichage.html")


def home(request):
    return render(request, "pages/home.html")


def create_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            ...  # sauver l'article
            form.save()
            return render(request, "pages/home.html#empty_modal")
    else:
        form = ArticleForm()
    return render(
        request,
        "pages/home.html#article_form",
        context={"form": form},
    )


class HomeView(View):
    def get(self, request):
        form = ArticleForm()
        return render(
            request,
            "pages/home.html",
            context={"form": form},
        )

    def post(self, request):
        form = ArticleForm(request.POST)
        if form.is_valid():
            ...  # traiter
            return redirect("pages:home")
        return render(
            request,
            "pages/home.html",
            context={"form": form},
        )


home_view = HomeView.as_view()
