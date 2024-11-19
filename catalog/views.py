from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Avg

from catalog.form import CustomUserCreationForm, FindingCreationForm, UserSerchForm, FindingSerchForm, FeedbackForm
from catalog.models import Finding, Collection, Image, Feedback


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

########################################################################

class UserListView(generic.ListView):
    model = get_user_model()
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = UserSerchForm(
            initial={"username": username},
        )
        return context

    def get_queryset(self):
        username = self.request.GET.get("username")
        if username:
            return super().get_queryset().filter(username__icontains=username)
        return super().get_queryset()


class UserDetailView(generic.DetailView):
    model = get_user_model()

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related("findings").all()
        return queryset

class UserCreateView(UserPassesTestMixin, generic.CreateView):
    model = get_user_model()
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("catalog:comrades")

    def test_func(self):
        return not self.request.user.is_authenticated


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = get_user_model()
    fields = ("first_name", "last_name", "detector_model", "photo")
    success_url = reverse_lazy("catalog:comrades")

    def test_func(self):
        user = self.get_object()
        return self.request.user == user or self.request.user.is_superuser

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(reverse_lazy("login"))
        messages.error(self.request, "only the account owner and superuser can edit this page")
        return redirect(reverse_lazy("catalog:comrades-detail", kwargs={"pk": self.get_object().pk}))


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("catalog:comrades")
    template_name = "catalog/confirm_delete.html"

    def test_func(self):
        user = self.get_object()
        return self.request.user == user or self.request.user.is_superuser

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(reverse_lazy("login"))
        messages.error(self.request, "only the account owner and superuser can edit this page")
        return redirect(reverse_lazy("catalog:comrades-detail", kwargs={"pk": self.get_object().pk}))

#########################################################################################################

class CollectionListView(generic.ListView):
    model = Collection
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related("findings")
        return queryset

class CollectionDetailView(generic.DetailView):
    model = Collection
    slug_field = "name"
    slug_url_kwarg = "coll_slag"

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related("findings")
        return queryset


class CollectionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Collection
    fields = "__all__"
    success_url = reverse_lazy("catalog:collections")


class CollectionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Collection
    fields = "__all__"
    success_url = reverse_lazy("catalog:collections")


class CollectionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Collection
    template_name = "catalog/confirm_delete.html"
    success_url = reverse_lazy("catalog:collections")


#####################################################################

class FindingsListView(generic.ListView):
    model = Finding
    paginate_by = 3


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = FindingSerchForm(
            initial={"name": name},
        )
        return context

    def get_queryset(self):
        name = self.request.GET.get("name")
        if name:
            return super().get_queryset().filter(name__icontains=name)
        return super().get_queryset()




class FindingsDetailView(generic.DetailView):
    model = Finding

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related(
            "images", "collections", "feedbacks",
        ).select_related("user").all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        finding = self.get_object()
        average_rating = finding.feedbacks.aggregate(Avg("rating"))["rating__avg"] or 0
        context["average_rating"] = round(average_rating, 1)
        reviewer = self.request.user
        context["feedback_form"] = FeedbackForm(
            initial={"reviewer": reviewer, "finding": finding},
        )
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Отримання поточного об'єкта
        form = FeedbackForm(request.POST)

        if form.is_valid():
            form.save()  # Збереження даних у базу
            return HttpResponseRedirect(
                reverse("catalog:findings-detail", kwargs={"pk": self.object.pk})
            )
        else:
            # Якщо форма недійсна, повертаємо її з помилками
            context = self.get_context_data()
            context["feedback_form"] = form
            return self.render_to_response(context)

class FindingsCreateView(LoginRequiredMixin, generic.CreateView):
    model = Finding
    form_class = FindingCreationForm
    success_url = reverse_lazy("catalog:findings")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

class FindingsUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Finding
    form_class = FindingCreationForm
    success_url = reverse_lazy("catalog:findings")

    def get_form_kwargs(self):
        # Отримуємо всі аргументи, передані в форму
        kwargs = super().get_form_kwargs()
        # Додаємо поточного користувача в аргументи
        kwargs['user'] = self.request.user
        return kwargs

class FindingsDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Finding
    template_name = "catalog/confirm_delete.html"
    success_url = reverse_lazy("catalog:findings")



class ImageCreateView(LoginRequiredMixin, generic.CreateView):
    model = Image
    fields = "__all__"
    success_url = reverse_lazy("catalog:findings")


class ImageDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Image
    template_name = "catalog/confirm_delete.html"
    success_url = reverse_lazy("catalog:findings")


def feedbacks_to_finding_view(request: HttpRequest, pk) -> HttpResponse:
    feedbacks = Feedback.objects.filter(finding__exact=pk)
    context = {"feedbacks": feedbacks}
    return render(request, "catalog/feedbacks_list.html", context=context)