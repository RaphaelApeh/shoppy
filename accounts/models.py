from django.db import models
from django.conf import settings

from django_countries.fields import CountryField

User = getattr(settings, "AUTH_USER_MODEL", "auth.User")


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = CountryField(null=True, blank=True, blank_label="(select country)")

    def __str__(self):
        return self.user.username
