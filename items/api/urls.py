from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    path("items/", views.ItemListView.as_view())
]

router = DefaultRouter()
router.register("user-items", views.UserItemView)
urlpatterns += router.get_urls()