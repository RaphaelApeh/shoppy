from django.views.generic import (
    ListView,
    CreateView
)
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins import ModelSearchMixin
from .forms import ItemForm
from .models import Item


class ItemListView(ModelSearchMixin, ListView):
    
    template_name = "items/items_list.html"
    queryset = Item.objects.select_related("user").order_by("-created_at", "-updated_at")
    search_fields = ["quantities", "user__username", "tags__name", "name"]
    distinct = True
    paginate_by = 10


class ItemCreateView(LoginRequiredMixin, CreateView):

    template_name = "items/items_create.html"
    model = Item
    form_class = ItemForm
