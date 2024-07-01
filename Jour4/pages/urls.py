from django.urls import path

from .views import home, home_view, create_article

app_name = "pages"

urlpatterns = [
    path("", home, name="home"),
    path("articles/create/", create_article, name="create-article"),
]
