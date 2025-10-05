from django.urls import path
from . import views

urlpatterns = [
    path("", views.schulklasse_list, name="schulklasse_list"),
    path("<int:pk>/inline/update/", views.schulklasse_inline_update, name="schulklasse_inline_update"),
    path("<int:pk>/inline/delete/", views.schulklasse_inline_delete, name="schulklasse_inline_delete"),
]
