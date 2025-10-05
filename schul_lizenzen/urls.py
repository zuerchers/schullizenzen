from django.contrib import admin
from django.urls import path, include
from lizenzen import views

urlpatterns = [
    path("admin/", admin.site.urls),

    # Root → Verwaltung
    path("", views.verwaltung_table, name="home"),

    # Alle App-Routen an einer Stelle
    path("", include("lizenzen.urls")),
]
