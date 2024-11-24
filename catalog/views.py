from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Avg
from django.forms.models import model_to_dict
from django.core.paginator import Paginator

from catalog.form import (
    CustomUserCreationForm,
    FindingCreationForm,
    UserSerchForm,
    FindingSerchForm,
    FeedbackForm,
    ImageForm,
)
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
    paginate_by = 7

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
        queryset = super().get_queryset().prefetch_related("findings__images").all()
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
        messages.error(
            self.request, "only the account owner and superuser can edit this page"
        )
        return redirect(
            reverse_lazy("catalog:comrades-detail", kwargs={"pk": self.get_object().pk})
        )


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
        messages.error(
            self.request, "only the account owner and superuser can edit this page"
        )
        return redirect(
            reverse_lazy("catalog:comrades-detail", kwargs={"pk": self.get_object().pk})
        )


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
    paginate_by = 7

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
        queryset = (
            super()
            .get_queryset()
            .prefetch_related(
                "images",
                "collections",
                "feedbacks",
            )
            .select_related("user")
            .all()
        )
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
        context["image_form"] = ImageForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        finding = self.object

        # Перевіряємо, яку форму було надіслано
        if "submit_feedback" in request.POST:  # Ідентифікатор кнопки
            feedback_form = FeedbackForm(request.POST)
            if feedback_form.is_valid():
                feedback_form.save()
                return HttpResponseRedirect(
                    reverse("catalog:findings-detail", kwargs={"pk": finding.pk})
                )
            else:
                # Повертаємо форму з помилками
                image_form = ImageForm()  # Порожня форма додавання фото
        elif "submit_image" in request.POST:  # Інший ідентифікатор кнопки
            image_form = ImageForm(request.POST, request.FILES)
            if image_form.is_valid():
                image = image_form.save(commit=False)
                image.finding = finding  # Прив'язка фото до знахідки
                image.save()
                return HttpResponseRedirect(
                    reverse("catalog:findings-detail", kwargs={"pk": finding.pk})
                )
            else:
                # Повертаємо форму з помилками
                feedback_form = FeedbackForm(
                    initial={"reviewer": request.user, "finding": finding}
                )
        else:
            # Якщо форма не визначена, повертаємо порожні форми
            feedback_form = FeedbackForm(
                initial={"reviewer": request.user, "finding": finding}
            )
            image_form = ImageForm()

        # Повертаємо обидві форми в контекст
        context = self.get_context_data()
        context["feedback_form"] = feedback_form
        context["image_form"] = image_form
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
        kwargs["user"] = self.request.user
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

    # def delete(self, request, *args, **kwargs):
    #     # Отримати об'єкт перед видаленням
    #     image = self.get_object()
    #
    #     # Оновлення зв'язаного об'єкта
    #     if image.finding:  # Перевірка, чи є зв'язок
    #         image.finding.some_field = None  # Або встановити значення за замовчуванням
    #         image.finding.save()
    #
    #     # Видалити зображення
    #     return super().delete(request, *args, **kwargs)


def feedbacks_to_finding_view(request: HttpRequest, pk) -> HttpResponse:
    feedbacks = Feedback.objects.filter(finding=pk)
    paginator = Paginator(feedbacks, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    is_paginated = page_obj.has_other_pages()
    context = {
        "feedbacks": feedbacks,
        "page_obj": page_obj,
        "is_paginated": is_paginated,
        "paginator": paginator,
    }
    return render(request, "catalog/feedbacks_list.html", context=context)
