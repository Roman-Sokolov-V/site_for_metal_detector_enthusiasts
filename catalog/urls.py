from django.urls import path

from catalog.views import (
    index,
    UserList,
    UserDetail,
    UserCreate,
    UserUpdate,
    CollectionList,
    CollectionDetail,
    CollectionCreate,
    CollectionUpdate,
    FindingsList,
    FindingsDetail,
    FindingsCreate,
    FindingsUpdate,
    FindingsDelete,
    ImageCreate,
    ImageDelete,
)


app_name = "catalog"

urlpatterns = [
    path("index/", index, name="index"),
    path("comrades/", UserList.as_view(), name="comrades"),
    path("comrades/<int:pk>/", UserDetail.as_view(), name="comrades-detail"),
    path("comrades/create/", UserCreate.as_view(), name="comrades-create"),
    path("comrades/<int:pk>/update/", UserUpdate.as_view(),
         name="comrades-update"),
    path("collections/create/", CollectionCreate.as_view(), name="collections-create"),
    path("collections/<int:pk>/update/", CollectionUpdate.as_view(), name="collections-update"),
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
    path("findings/create", FindingsCreate.as_view(), name="findings-create"),
    path("findings/<int:pk>/update/", FindingsUpdate.as_view(), name="findings-update"),
    path("findings/<int:pk>/delele/", FindingsDelete.as_view(), name="findings-delete"),
    path("image/create/", ImageCreate.as_view(), name="image-create"),
    path("image/<int:pk>/delele/", ImageDelete.as_view(), name="image-delete"),
    ]