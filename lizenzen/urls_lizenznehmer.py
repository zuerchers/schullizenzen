from django.urls import path
from . import views

urlpatterns = [
    path("", views.lizenznehmer_list, name="lizenznehmer_list"),
    path("<int:pk>/inline/update/", views.lizenznehmer_inline_update, name="lizenznehmer_inline_update"),
    path("<int:pk>/inline/delete/", views.lizenznehmer_inline_delete, name="lizenznehmer_inline_delete"),
]
