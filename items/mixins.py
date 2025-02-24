from django.db.models import Q


class ModelSearchMixin:

    search_fields = None
    query_param = "q"
    distinct = False
    lookups = {
        "^": "startswith"
    }

    def get_search_fields(self)-> list[str]:
        
        assert isinstance(self.search_fields, (tuple, list)), "'search_fields' must be of type tuple or list"
        return self.search_fields

    
    @property
    def get_query_param(self)-> str:
        return self.request.GET.get(self.query_param, None)

    def process_lookup(self):
        values = []
        for field_name in self.get_search_fields():
            for key, value in self.lookups.items():
                if field_name.startswith(key):
                    if (field_name, value) not in values:
                        field_name = field_name.removeprefix(key)
                        values.append((field_name, value))
                        break
                else:
                    if (field_name, value) not in values:
                        values.append((field_name, value))
                        break
        print(values)
        return values   

    def search_field(self, queryset):
        
        assert self.query_param is not None, f"{self.__class__.__name__} must have 'query_param' attribute."
        search_lookup = self.get_query_param
        
        assert search_lookup is not None, "'query_param' can't be of type None"
        value = search_lookup.strip()
        query = Q()
        for field, lookup in self.process_lookup():
            assert field and lookup is not None
            query |= Q(**{f"{field}__{lookup}": value})
        print(query)
        queryset = queryset.filter(query)
        if self.distinct:
            queryset = queryset.filter(query).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.query_param] = self.get_query_param
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        
        if self.search_fields and self.request.GET.get(self.query_param):
            return self.search_field(queryset)
        return queryset
