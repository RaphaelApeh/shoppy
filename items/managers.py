from django.db.models import (
    QuerySet,
    Manager
)

class ItemQuerySet(QuerySet):

    def user_items(self, user, distinct=False, **kwargs):

        queryset = self.filter(user=user, **kwargs)
        if distinct:
            queryset = queryset.distinct()
        return queryset
    
    def inactive_items(self):
        
        return self.filter(active=False)


class ItemManager(Manager):

    def get_queryset(self):
        return ItemQuerySet(self.model, using=self._db)
    
    def inactive_items(self):
        
        return self.get_queryset().inactive_items()
    
    def user_items(self, user, distinct=False, **kwargs):

        return self.get_queryset().user_items(user, distinct, **kwargs)