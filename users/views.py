from django.shortcuts import render, redirect
from django.views.generic import View, CreateView
from django.contrib.auth import login

from .forms import UserCreationForm


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("pages:home")
    else:
        form = UserCreationForm()

    return render(
        request,
        "users/signup.html",
        context={
            "form": form,
        },
    )