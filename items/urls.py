from django.urls import path

from . import views

app_name: str = "items"

urlpatterns: list[path] = [
    path("items/", views.ItemListView.as_view())

]