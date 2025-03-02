from django.urls import path

from . import views

app_name: str = "items"

urlpatterns: list[path] = [
    path("items/", views.ItemListView.as_view(), name="items_list"),
    path(
        "items/<str:slug>",
        views.ItemDetailView.as_view(),
        name="items_detail"
    ),
    path(
        "items/<str:slug>/update",
        views.ItemUpdateView.as_view(),
        name="items_update"
    )

]