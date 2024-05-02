from django.db import models
from django.contrib.auth.models import User


class UserAdditional(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="owner")
    portfolio_link = models.CharField(max_length=200, blank=True, null=True, verbose_name="portfolio link")
