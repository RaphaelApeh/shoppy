from django.db.models import Manager, QuerySet


class ItemQuerySet(QuerySet):

    def user_items(self, user, distinct=False, **kwargs):

        queryset = self.filter(user=user, **kwargs)
        if distinct:
            queryset = queryset.distinct()
        return queryset
    
    def inactive_items(self):
        
        return self.filter(active=False)

    def filter_by_user_country(self, user):

        return self.filter(user__profile__country__name=user.profile.country.name)

class ItemManager(Manager):

    def get_queryset(self):
        return ItemQuerySet(self.model, using=self._db)
    
    def inactive_items(self):
        
        return self.get_queryset().inactive_items()
    
    def user_items(self, user, distinct=False, **kwargs):

        return self.get_queryset().user_items(user, distinct, **kwargs)
    
    def filter_by_user_country(self, user):

        return self.get_queryset().filter_by_user_country(user)