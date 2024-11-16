from django.urls import path

from catalog.views import (
    index,
    UserListView,
    UserDetailView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
    CollectionListView,
    CollectionDetailView,
    CollectionCreateView,
    CollectionUpdateView,
    CollectionDeleteView,
    FindingsListView,
    FindingsDetailView,
    FindingsCreateView,
    FindingsUpdateView,
    FindingsDeleteView,
    ImageCreateView,
    ImageDeleteView,
)


app_name = "catalog"

urlpatterns = [
    path("index/", index, name="index"),
    path("comrades/", UserListView.as_view(), name="comrades"),
    path("comrades/<int:pk>/", UserDetailView.as_view(), name="comrades-detail"),
    path("comrades/create/", UserCreateView.as_view(), name="comrades-create"),
    path("comrades/<int:pk>/update/", UserUpdateView.as_view(),
         name="comrades-update"),
    path("comrades/<int:pk>/delele/",  UserDeleteView.as_view(), name="comrades-delete"),
    path("collections/create/", CollectionCreateView.as_view(), name="collections-create"),
    path("collections/<int:pk>/update/", CollectionUpdateView.as_view(), name="collections-update"),
    path("collections/", CollectionListView.as_view(), name="collections"),
    path(
        "collections/<slug:coll_slag>/",
        CollectionDetailView.as_view(),
        name="collections-detail"
    ),
    path("collections/<int:pk>/delele/",  CollectionDeleteView.as_view(), name="collections-delete"),

    path("findings/", FindingsListView.as_view(), name="findings"),
    path(
        "findings/<int:pk>/",
        FindingsDetailView.as_view(),
        name="findings-detail"
    ),
    path("findings/create", FindingsCreateView.as_view(), name="findings-create"),
    path("findings/<int:pk>/update/", FindingsUpdateView.as_view(), name="findings-update"),
    path("findings/<int:pk>/delele/", FindingsDeleteView.as_view(), name="findings-delete"),
    path("image/create/", ImageCreateView.as_view(), name="image-create"),
    path("image/<int:pk>/delele/", ImageDeleteView.as_view(), name="image-delete"),
    ]