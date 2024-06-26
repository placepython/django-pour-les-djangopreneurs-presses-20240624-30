from django.shortcuts import render


def home(request):
    ... # rechercher de l'info en base de données

    return render(
        request,
        "pages/home.html",
    )
