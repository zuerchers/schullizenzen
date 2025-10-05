from django.urls import path
from . import views

urlpatterns = [
    path("", views.software_list, name="software_list"),
    path("<int:pk>/inline/update/", views.software_inline_update, name="software_inline_update"),
    path("<int:pk>/inline/delete/", views.software_inline_delete, name="software_inline_delete"),
]
