from django.views.generic import (
    ListView,
    CreateView,
    DetailView
)
from django.db import connection
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins import ModelSearchMixin
from .forms import ItemForm
from .models import Item


class ItemListView(ModelSearchMixin, ListView):
    
    template_name = "items/items_list.html"
    queryset = Item.objects.select_related("user").order_by("-created_at", "-updated_at")
    search_fields = ["quantities", "user__username", "tags__name", "name"]
    distinct = True
    paginate_by = 5


class ItemDetailView(DetailView):

    template_name = "items/items_detail.html"
    model = Item
    queryset = Item.objects.select_related("user")
    
    def get_queryset(self):
        qs = super().get_queryset()
        print(connection.queries)
        return qs

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context["user_related_items"] = self.get_queryset().user_items(obj.user).exclude(pk=obj.pk)

        return context


class ItemCreateView(LoginRequiredMixin, CreateView):

    template_name = "items/items_create.html"
    model = Item
    form_class = ItemForm
