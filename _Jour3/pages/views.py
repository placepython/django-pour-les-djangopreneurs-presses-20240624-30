from django.shortcuts import render, redirect
from django.views.generic import View

from blog.forms import ArticleForm


def home(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            ...  # traiter
            return redirect("pages:home")
    else:
        form = ArticleForm()
    return render(
        request,
        "pages/home.html",
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
