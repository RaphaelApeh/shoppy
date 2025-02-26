from django.views.generic import ListView

from .mixins import ModelSearchMixin
from .models import Item


class ItemListView(ModelSearchMixin, ListView):
    
    template_name = "items/items_list.html"
    queryset = Item.objects.all()
    search_fields = ["quantities", "user__username", "tags__name", "name"]
    distinct = True
    