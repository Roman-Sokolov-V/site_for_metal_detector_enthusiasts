import django.contrib.auth
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.contrib.auth import get_user_model
from django.views import generic

from catalog.models import Finding, Collection

def index(request: HttpRequest) -> HttpResponse:
    num_findings = Finding.objects.count()
    num_collections = Collection.objects.count()
    num_comrades = get_user_model().objects.count()
    context = {
        "num_findings": num_findings,
        "num_collections": num_collections,
        "num_comrades": num_comrades,
    }
    return render(request, "catalog/index.html", context=context)


class UserList(generic.ListView):
    model = get_user_model()

class UserDetail(generic.DetailView):
    model = get_user_model()

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related("findings").all()
        return queryset


class CollectionList(generic.ListView):
    model = Collection

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related("findings").all()
        return queryset