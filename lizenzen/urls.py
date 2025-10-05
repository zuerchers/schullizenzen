
from django.urls import path, include
from . import views

urlpatterns = [
    # Verwaltung
    path("verwaltung/", views.verwaltung_table, name="verwaltung_table"),
    path("verwaltung/create/", views.verwaltung_create, name="verwaltung_create"),
    path("verwaltung/<int:pk>/inline/update/", views.verwaltung_inline_update, name="verwaltung_inline_update"),
    path("verwaltung/<int:pk>/inline/delete/", views.verwaltung_inline_delete, name="verwaltung_inline_delete"),

    # FK create (für Modals im Verwaltung-Insert)
    path("lizenznehmer/create/", views.lizenznehmer_create, name="lizenznehmer_create"),
    path("software/create/", views.software_create, name="software_create"),
    path("kostentyp/create/", views.kostentyp_create, name="kostentyp_create"),
    path("schuleinheit/create/", views.schuleinheit_create, name="schuleinheit_create"),
    path("schulklasse/create/", views.schulklasse_create, name="schulklasse_create"),

    # FK Tabellen mit Inline-Edit
    path("lizenznehmer/", views.lizenznehmer_list, name="lizenznehmer_list"),
    path("lizenznehmer/<int:pk>/inline/update/", views.lizenznehmer_inline_update, name="lizenznehmer_inline_update"),
    path("lizenznehmer/<int:pk>/inline/delete/", views.lizenznehmer_inline_delete, name="lizenznehmer_inline_delete"),

    path("software/", views.software_list, name="software_list"),
    path("software/<int:pk>/inline/update/", views.software_inline_update, name="software_inline_update"),
    path("software/<int:pk>/inline/delete/", views.software_inline_delete, name="software_inline_delete"),

    path("kostentyp/", views.kostentyp_list, name="kostentyp_list"),
    path("kostentyp/<int:pk>/inline/update/", views.kostentyp_inline_update, name="kostentyp_inline_update"),
    path("kostentyp/<int:pk>/inline/delete/", views.kostentyp_inline_delete, name="kostentyp_inline_delete"),

    path("schuleinheit/", views.schuleinheit_list, name="schuleinheit_list"),
    path("schuleinheit/<int:pk>/inline/update/", views.schuleinheit_inline_update, name="schuleinheit_inline_update"),
    path("schuleinheit/<int:pk>/inline/delete/", views.schuleinheit_inline_delete, name="schuleinheit_inline_delete"),

    path("schulklasse/", views.schulklasse_list, name="schulklasse_list"),
    path("schulklasse/<int:pk>/inline/update/", views.schulklasse_inline_update, name="schulklasse_inline_update"),
    path("schulklasse/<int:pk>/inline/delete/", views.schulklasse_inline_delete, name="schulklasse_inline_delete"),
]
