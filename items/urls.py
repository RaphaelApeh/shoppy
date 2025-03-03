from django.urls import path

from . import views

app_name: str = "items"

urlpatterns: list[path] = [
    path("items/", views.ItemListView.as_view(), name="items_list"),
    path(
        "new/",
        views.ItemCreateView.as_view(),
        name="items_create"
    ),
    path(
        "items/<str:slug>/",
        views.ItemDetailView.as_view(),
        name="items_detail"
    ),
    path(
        "items/<str:slug>/update/",
        views.ItemUpdateView.as_view(),
        name="items_update"
    ),
    path(
        "items/<str:slug>/delete/",
        views.ItemDeleteView.as_view(),
        name="items_delete"
    ),
    path("items/<str:slug>/description/", views.show_full_description_view, name="items_description")

]