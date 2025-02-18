from django.db import models
from django.conf import settings

User = getattr(settings, "AUTH_USER_MODEL", "auth.User")

"""
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.user.username
"""