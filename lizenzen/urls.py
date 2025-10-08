from django.urls import path
from . import views

urlpatterns = [
    # --- Hauptseiten ---
    path("", views.verwaltung_table, name="home"),
    path("verwaltung/", views.verwaltung_table, name="verwaltung_table"),

    # --- Verwaltung CRUD ---
    path("verwaltung/create/", views.verwaltung_create, name="verwaltung_create"),
    path("verwaltung/<int:pk>/inline/update/", views.verwaltung_inline_update, name="verwaltung_inline_update"),
    path("verwaltung/<int:pk>/inline/delete/", views.verwaltung_inline_delete, name="verwaltung_inline_delete"),

    # --- FK Listen ---
    path("lizenznehmer/", views.lizenznehmer_list, name="lizenznehmer_list"),
    path("software/", views.software_list, name="software_list"),
    path("kostentyp/", views.kostentyp_list, name="kostentyp_list"),
    path("schuleinheit/", views.schuleinheit_list, name="schuleinheit_list"),
    path("schulklasse/", views.schulklasse_list, name="schulklasse_list"),

    # --- FK Create ---
    path("lizenznehmer/create/", views.lizenznehmer_create, name="lizenznehmer_create"),
    path("software/create/", views.software_create, name="software_create"),
    path("kostentyp/create/", views.kostentyp_create, name="kostentyp_create"),
    path("schuleinheit/create/", views.schuleinheit_create, name="schuleinheit_create"),
    path("schulklasse/create/", views.schulklasse_create, name="schulklasse_create"),

    # --- FK Inline Update/Delete ---
    path("lizenznehmer/<int:pk>/inline/update/", views.lizenznehmer_inline_update, name="lizenznehmer_inline_update"),
    path("lizenznehmer/<int:pk>/inline/delete/", views.lizenznehmer_inline_delete, name="lizenznehmer_inline_delete"),

    path("software/<int:pk>/inline/update/", views.software_inline_update, name="software_inline_update"),
    path("software/<int:pk>/inline/delete/", views.software_inline_delete, name="software_inline_delete"),

    path("kostentyp/<int:pk>/inline/update/", views.kostentyp_inline_update, name="kostentyp_inline_update"),
    path("kostentyp/<int:pk>/inline/delete/", views.kostentyp_inline_delete, name="kostentyp_inline_delete"),

    path("schuleinheit/<int:pk>/inline/update/", views.schuleinheit_inline_update, name="schuleinheit_inline_update"),
    path("schuleinheit/<int:pk>/inline/delete/", views.schuleinheit_inline_delete, name="schuleinheit_inline_delete"),

    path("schulklasse/<int:pk>/inline/update/", views.schulklasse_inline_update, name="schulklasse_inline_update"),
    path("schulklasse/<int:pk>/inline/delete/", views.schulklasse_inline_delete, name="schulklasse_inline_delete"),

    # --- Verwaltung Exports ---
    path("verwaltung/export/xlsx/", views.verwaltung_export_xlsx, name="verwaltung_export_xlsx"),
    path("verwaltung/export/pdf/", views.verwaltung_export_pdf, name="verwaltung_export_pdf"),

    # --- FK Exports (gemeinsame Views) ---
    path("lizenznehmer/export/xlsx/", views.fk_export_xlsx, {"model_name": "lizenznehmer"}, name="lizenznehmer_export_xlsx"),
    path("lizenznehmer/export/pdf/", views.fk_export_pdf, {"model_name": "lizenznehmer"}, name="lizenznehmer_export_pdf"),

    path("software/export/xlsx/", views.fk_export_xlsx, {"model_name": "software"}, name="software_export_xlsx"),
    path("software/export/pdf/", views.fk_export_pdf, {"model_name": "software"}, name="software_export_pdf"),

    path("kostentyp/export/xlsx/", views.fk_export_xlsx, {"model_name": "kostentyp"}, name="kostentyp_export_xlsx"),
    path("kostentyp/export/pdf/", views.fk_export_pdf, {"model_name": "kostentyp"}, name="kostentyp_export_pdf"),

    path("schuleinheit/export/xlsx/", views.fk_export_xlsx, {"model_name": "schuleinheit"}, name="schuleinheit_export_xlsx"),
    path("schuleinheit/export/pdf/", views.fk_export_pdf, {"model_name": "schuleinheit"}, name="schuleinheit_export_pdf"),

    path("schulklasse/export/xlsx/", views.fk_export_xlsx, {"model_name": "schulklasse"}, name="schulklasse_export_xlsx"),
    path("schulklasse/export/pdf/", views.fk_export_pdf, {"model_name": "schulklasse"}, name="schulklasse_export_pdf"),
]
