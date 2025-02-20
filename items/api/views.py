from django_filters import rest_framework as filters
from rest_framework import generics

from items.models import Item
from items.filters import ItemFilter

from .serializers import ItemSerializer


class ItemListView(generics.ListAPIView):
    """
    List of users items
    """

    serializer_class = ItemSerializer
    queryset = Item.objects.select_related("user")
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ItemFilter