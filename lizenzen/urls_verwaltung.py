from django.urls import path
from . import views

urlpatterns = [
    path("table/", views.verwaltung_table, name="verwaltung_table"),
    path("create/", views.verwaltung_create, name="verwaltung_create"),
    path("<int:pk>/inline/update/", views.verwaltung_inline_update, name="verwaltung_inline_update"),
    path("<int:pk>/inline/delete/", views.verwaltung_inline_delete, name="verwaltung_inline_delete"),
]
