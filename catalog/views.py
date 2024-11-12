import django.contrib.auth
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views import generic

from catalog.models import Finding, Collection

def index(request: HttpRequest) -> HttpResponse:
    num_findings = Finding.objects.count()
    num_collections = Collection.objects.count()
    num_comrades = get_user_model().objects.count()
    num_visits = request.session.get("visits", 0)
    request.session["visits"] = num_visits + 1
    context = {
        "num_findings": num_findings,
        "num_collections": num_collections,
        "num_comrades": num_comrades,
        "num_visits": num_visits,
    }
    return render(request, "catalog/index.html", context=context)


class UserList(generic.ListView):
    model = get_user_model()

class UserDetail(generic.DetailView):
    model = get_user_model()

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related("findings").all()
        return queryset

class UserCreate(generic.CreateView):
    model = get_user_model()
    fields = ("username", "password", "first_name",
              "last_name", "detector_model")
    success_url = reverse_lazy("catalog:comrades")


class UserUpdate(generic.UpdateView):
    model = get_user_model()
    fields = ("first_name", "last_name", "detector_model", "photo")
    success_url = reverse_lazy("catalog:comrades")


class CollectionList(generic.ListView):
    model = Collection

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related("findings")
        return queryset

class CollectionDetail(generic.DetailView):
    model = Collection
    slug_field = "name"
    slug_url_kwarg = "coll_slag"

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related("findings")
        return queryset


class FindingsList(generic.ListView):
    model = Finding


class FindingsDetail(generic.DetailView):
    model = Finding

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related(
            "images", "collections", "feedbacks",
        ).select_related("user").all()
        return queryset