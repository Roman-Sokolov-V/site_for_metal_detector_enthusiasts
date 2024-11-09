from django.contrib import admin
from django.urls import path, include

from catalog.views import index


app_name = "catalog"

urlpatterns = [
    path("index/", index, name="index")
]
