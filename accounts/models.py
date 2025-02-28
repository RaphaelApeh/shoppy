from django.db import models
from django.conf import settings
from django.db.models.signals import (
    post_save,
    pre_save
)
from django.dispatch import receiver

from django_countries.fields import CountryField

User = getattr(settings, "AUTH_USER_MODEL", "auth.User")


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = CountryField(null=True, blank=True, blank_label="(select country)")

    def __str__(self):
        return self.user.username

@receiver([post_save, pre_save], sender=User)
def create_user_profile(sender, instance, created=None, **kwargs):
 
    if created:
        Profile.objects.create(user=instance)