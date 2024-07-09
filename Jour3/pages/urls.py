from django.urls import path

from .views import home, home_view

app_name = "pages"

urlpatterns = [
    path("", home, name="home"),
]
