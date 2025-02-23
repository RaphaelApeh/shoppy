from django.core.exceptions import ImproperlyConfigured

from .models import Profile


class ProfileMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not hasattr(request, "user")and not hasattr(request.user, "profile"):
            raise ImproperlyConfigured
        if request.user.is_authenticated:
            request.profile = UserProfile(request)
        else:
            request.profile = None
        return self.get_response(request)

class UserProfile:

    def __init__(self, request):
        self.request = request
        self.profile = request.user.profile

    def __eq__(self, other: Profile):
        if not isinstance(other, Profile):
            raise
        return self.profile.pk == other.pk
        
    def __getattr__(self, name: str):
        user_profile = self.request.user.profile
        if not hasattr(user_profile, name):
            raise
        return getattr(user_profile, name)
    
    def __str__(self):
        return str(self.profile)
    
    def __repr__(self):
        return  repr(self.profile)
