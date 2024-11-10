from django.contrib import admin
from django.urls import path, include

from catalog.views import index, UserList


app_name = "catalog"

urlpatterns = [
    path("index/", index, name="index"),
    path("comrades/", UserList.as_view(), name="comrades"),
    ]