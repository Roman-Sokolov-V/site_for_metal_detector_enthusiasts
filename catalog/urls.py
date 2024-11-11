from catalog.models import Collection
from django.contrib import admin
from django.urls import path, include

from catalog.views import (
    index,
    UserList,
    UserDetail,
    CollectionList,
    CollectionDetail,
    FindingsList,
    FindingsDetail,
)


app_name = "catalog"

urlpatterns = [
    path("index/", index, name="index"),
    path("comrades/", UserList.as_view(), name="comrades"),
    path("comrades/<int:pk>/", UserDetail.as_view(), name="comrades-detail"),
    path("collections/", CollectionList.as_view(), name="collections"),
    path(
        "collections/<slug:coll_slag>/",
        CollectionDetail.as_view(),
        name="collections-detail"
    ),
    path("findings/", FindingsList.as_view(), name="findings"),
    path(
        "findings/<int:pk>/",
        FindingsDetail.as_view(),
        name="findings-detail"
    ),
    ]