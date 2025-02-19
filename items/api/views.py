from rest_framework import generics

from items.models import Item

from .serializers import ItemSerializer


class ItemListView(generics.ListAPIView):
    """
    List of users items
    """

    serializer_class = ItemSerializer
    queryset = Item.objects.select_related("user")
    
    def get_queryset(self):
        return super().get_queryset().order_by("-views", "-updated_at")