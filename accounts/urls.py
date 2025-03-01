from django.urls import path, include

from . import views

urlpatterns = [
    path("", include("allauth.urls")),

    path(
        "profile/",
        views.UserProfile.as_view(),
        name="account_profile"
    )
]