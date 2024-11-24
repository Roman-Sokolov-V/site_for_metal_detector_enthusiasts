import catalog.models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from catalog.models import User, Finding, Image, Collection, Feedback


@admin.register(User)
class ComradAdmin(UserAdmin):
    list_display = ("username", "email", "is_staff", "date_joined", "detector_model")
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("detector_model",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional info", {"fields": ("first_name", "last_name", "detector_model")}),
    )


@admin.register(Finding)
class FindingAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
        "location",
        "date_found",
    )
    list_filter = (
        "collections",
        "user",
        "location",
        "date_found",
    )
    search_fields = ("name", "location", "description")


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "reviewer",
        "finding",
        "rating",
        "comment",
    )
    list_filter = (
        "finding",
        "rating",
    )
    search_fields = ("reviewer__username", "finding__name", "comment")


admin.site.register(Image)
admin.site.register(Collection)
