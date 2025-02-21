from django.views.generic import (
    ListView
)

from .models import Item
from .mixins import ModelSearchMixin


class ItemListView(ModelSearchMixin, ListView):
    
    template_name = "items/items_list.html"
    queryset = Item.objects.all()
    search_fields = ["quantities", "user__username", "tags__name", "name"]
    query_param = "apeh"