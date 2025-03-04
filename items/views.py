from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import ItemForm
from .mixins import ModelSearchMixin
from .models import Item


class ItemListView(ModelSearchMixin, ListView):
    
    template_name = "items/items_list.html"
    queryset = Item.objects.select_related("user").order_by("-created_at", "-updated_at").exclude(active=False).filter(quantities__gte=1)
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
        qs = self.get_queryset().user_items(obj.user).exclude(pk=obj.pk)
        paginator = Paginator(qs, per_page=4)
        context["user_related_items"] = paginator.get_page(int(self.request.GET.get("page", 1)))

        return context


class ItemCreateView(LoginRequiredMixin, CreateView):

    template_name = "items/items_create.html"
    model = Item
    form_class = ItemForm
    

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return redirect(obj.get_absolute_url())


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
    

class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    template_name = "items/partials/item_delete.html"
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        obj = get_object_or_404(self.model, slug=kwargs["slug"])
        if obj.user != request.user:
            return HttpResponseBadRequest()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["path"] = self.request.path
        return context


def show_full_description_view(request, slug: str):
    obj = get_object_or_404(Item, slug=slug)
    context = {
        "object": obj
    }
    return render(request, "items/partials/show_description.html", context)