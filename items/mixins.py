from typing import Any

from django.db.models import (
    Q,
    QuerySet
)

class ModelSearchMixin:

    """ Search model fields """

    search_fields = None
    query_param = "q"
    distinct = False

    def get_search_fields(self)-> list[str]:
        
        assert isinstance(self.search_fields, (tuple, list)), "'search_fields' must be of type tuple or list"
        return self.search_fields

    
    @property
    def get_query_param(self)-> dict[str, str]:
        return self.request.GET.copy()

    def search_field(self, queryset)-> QuerySet:
        
        def get_field(field_name: str)-> str:

            if field_name.startswith("^"):
                return "%s__startswith" % field_name.removeprefix("^")
            
            if field_name.startswith("="):
                return "%s__iexact" % field_name.removeprefix("=")
            
            if field_name.startswith("<"):
                return "%s__lt" % field_name.removeprefix("<")
            
            if field_name.startswith(">"):
                return "%s__gt" % field_name.removeprefix(">")
            
            return "%s__icontains" % field_name

        assert self.query_param is not None, f"{self.__class__.__name__} must have 'query_param' attribute."
        search_lookup = self.get_query_param.get(self.query_param)
        
        assert search_lookup is not None, "'query_param' can't be of type None"
        value = search_lookup.strip()
        query = Q()
        for field in self.get_search_fields():
            query |= Q(**{get_field(field): value})
        queryset = queryset.filter(query)
        # print(queryset.query)
        if self.distinct:
            queryset = queryset.filter(query).distinct()
        return queryset

    def get_context_data(self, **kwargs)-> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["search"] = self.query_param
        context[self.query_param] = self.get_query_param
        return context

    def get_queryset(self)-> QuerySet:
        queryset = super().get_queryset()
        
        if self.search_fields and self.request.GET.get(self.query_param):
            return self.search_field(queryset)
        return queryset
