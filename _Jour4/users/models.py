from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """L'utilisateur de mon application"""
    email = models.EmailField("user email address", unique=True)
