from django.shortcuts import render, redirect
from django.views.generic import View, CreateView
from django.contrib.auth import login

from .forms import UserCreationForm


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return render(request, "registration/login.html#signup-modal")
    else:
        form = UserCreationForm()

    return render(
        request,
        "registration/login.html#signup-form",
        context={
            "form": form,
        },
    )