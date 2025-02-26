from django_filters import rest_framework as filters
from rest_framework import generics, permissions, viewsets

from items.filters import ItemFilter
from items.models import Item

from .permissions import IsOwnerOrIsStaff
from .serializers import ItemSerializer


class ItemListView(generics.ListAPIView):
    """
    List of users items
    """

    serializer_class = ItemSerializer
    queryset = Item.objects.select_related("user", "user__profile")
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ItemFilter
    permission_classes = [permissions.IsAdminUser]


class UserItemView(viewsets.ModelViewSet):

    queryset = Item.objects.select_related("user", "user__profile")
    serializer_class = ItemSerializer
    permission_classes = [IsOwnerOrIsStaff, permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)