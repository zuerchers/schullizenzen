from django.urls import path
from . import views

urlpatterns = [
    path("", views.kostentyp_list, name="kostentyp_list"),
    path("<int:pk>/inline/update/", views.kostentyp_inline_update, name="kostentyp_inline_update"),
    path("<int:pk>/inline/delete/", views.kostentyp_inline_delete, name="kostentyp_inline_delete"),
]
