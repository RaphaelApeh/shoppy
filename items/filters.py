import django_filters
from django.db.models import Count

from .models import Item

class ItemFilter(django_filters.FilterSet):

    tags = django_filters.CharFilter("tags__name", lookup_expr="icontains")
    popular = django_filters.NumberFilter(method="view_user_count", label="Popular")


    class Meta:
        model = Item
        fields = {
             "name": ["iexact", "icontains"],
             "price": ["lt", "gt"],
             "quantities": ["gte"],
        }
        
        exclude = ["image"]

    def view_user_count(self, queryset, name, value):
        
        return queryset.annotate(view_count=Count("views")).filter(view_count__gte=value)