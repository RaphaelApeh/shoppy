from django.db.models.query import Q


class ModelSearchMixin:

    search_fields = None
    query_param = "q"

    def get_search_fields(self):
        
        assert isinstance(self.search_fields, (tuple, list)), "'search_fields' must be of type tuple or list"
        return self.search_fields
    
    def search_field(self, queryset):      
        
        search_lookup = self.request.GET.get(self.query_param, None)
        
        assert search_lookup is not None, "'query_param' can't be of type None"
        query = Q()
        for field in self.get_search_fields():
            query |= Q(**{f"{field}__icontains": search_lookup.strip()})

        return queryset.filter(query).distinct()
    
    def get_queryset(self):
        queryset = super().get_querset()
        
        if self.search_fields and self.request.GET.get(self.query_param):
            return self.search_field(queryset)
        return queryset
