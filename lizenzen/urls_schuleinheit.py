from django.urls import path
from . import views

urlpatterns = [
    path("", views.schuleinheit_list, name="schuleinheit_list"),
    path("<int:pk>/inline/update/", views.schuleinheit_inline_update, name="schuleinheit_inline_update"),
    path("<int:pk>/inline/delete/", views.schuleinheit_inline_delete, name="schuleinheit_inline_delete"),
]
