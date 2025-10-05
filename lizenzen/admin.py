from django.contrib import admin
from .models import (
    Verwaltung,
    Lizenznehmer,
    Software,
    Kostentyp,
    Schuleinheit,
    Schulklasse,
)


@admin.register(Verwaltung)
class VerwaltungAdmin(admin.ModelAdmin):
    list_display = (
        "lizenznehmer",
        "software",
        "kostentyp",
        "lizenz_start",
        "lizenz_ende",
        "schulklasse",
        "anzahl_weitere_lizenzen",
    )
    list_filter = ("software", "kostentyp", "lizenz_start", "lizenz_ende", "schulklasse")
    search_fields = ("lizenznehmer__name", "software__name", "kostentyp__bezeichnung")


@admin.register(Lizenznehmer)
class LizenznehmerAdmin(admin.ModelAdmin):
    list_display = ("name", "schuleinheit")
    list_filter = ("schuleinheit",)
    search_fields = ("name",)


@admin.register(Software)
class SoftwareAdmin(admin.ModelAdmin):
    list_display = ("name", "url")
    search_fields = ("name", "url")


@admin.register(Kostentyp)
class KostentypAdmin(admin.ModelAdmin):
    list_display = ("bezeichnung",)
    search_fields = ("bezeichnung",)


@admin.register(Schuleinheit)
class SchuleinheitAdmin(admin.ModelAdmin):
    list_display = ("bezeichnung",)
    search_fields = ("bezeichnung",)


@admin.register(Schulklasse)
class SchulklasseAdmin(admin.ModelAdmin):
    list_display = ("name", "anzahl_schueler")
    search_fields = ("name",)
