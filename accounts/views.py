from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render


class UserProfile(
    LoginRequiredMixin,
    View
    ):
    
    def get(self, request):
    
        return render(request, "accounts/profile.html")