from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views import generic

from catalog.form import CustomUserCreationForm
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
    paginate_by = 1

class UserDetail(generic.DetailView):
    model = get_user_model()

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related("findings").all()
        return queryset

class UserCreate(UserPassesTestMixin, generic.CreateView):
    model = get_user_model()
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("catalog:comrades")

    def test_func(self):
        return not self.request.user.is_authenticated




class UserUpdate(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = get_user_model()
    fields = ("first_name", "last_name", "detector_model", "photo")
    success_url = reverse_lazy("catalog:comrades")

    def test_func(self):
        user = self.get_object()
        return self.request.user == user or self.request.user.is_superuser

    def handle_no_permission(self):
        # Якщо користувач неавторизований, перенаправляємо на сторінку логіну
        if not self.request.user.is_authenticated:
            return redirect(reverse_lazy("login"))  # замініть "login" на ім'я вашої URL-сторінки логіну

        # Якщо авторизований користувач не має доступу, показуємо повідомлення і перенаправляємо
        messages.error(self.request, "only the account owner and superuser can edit this page")
        return redirect(reverse("catalog:comrades-detail", kwargs={"pk": self.get_object().pk}))



class CollectionList(generic.ListView):
    model = Collection
    paginate_by = 1

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
    paginate_by = 1


class FindingsDetail(generic.DetailView):
    model = Finding

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related(
            "images", "collections", "feedbacks",
        ).select_related("user").all()
        return queryset

