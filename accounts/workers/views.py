from django.views.generic import View
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator


@method_decorator(staff_member_required, "dispatch")
class ItemManagementView(View):

    def get(self, request, *args, **kwargs):
        
        context = {}
        return render(request, "workers/manage.html", context)