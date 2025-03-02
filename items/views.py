from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView
)
from django.http import HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins import ModelSearchMixin
from .forms import ItemForm
from .models import Item


class ItemListView(ModelSearchMixin, ListView):
    
    template_name = "items/items_list.html"
    queryset = Item.objects.select_related("user").order_by("-created_at", "-updated_at")
    search_fields = ["quantities", "^user__username", "tags__name", "name"]
    distinct = True
    paginate_by = 5


class ItemDetailView(DetailView):

    template_name = "items/items_detail.html"
    model = Item
    queryset = Item.objects.select_related("user")


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context["user_related_items"] = self.get_queryset().user_items(obj.user).exclude(pk=obj.pk)

        return context


class ItemCreateView(LoginRequiredMixin, CreateView):

    template_name = "items/items_create.html"
    model = Item
    form_class = ItemForm


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    template_name = "items/partials/item_update.html"
    form_class = ItemForm

    def dispatch(self, request, *args, **kwargs):
        if request.user != self.get_object().user:
            return HttpResponseBadRequest()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["path"] = self.request.path
        return context