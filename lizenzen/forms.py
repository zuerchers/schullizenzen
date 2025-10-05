
from django import forms
from .models import Verwaltung, Lizenznehmer, Software, Kostentyp, Schuleinheit, Schulklasse

class VerwaltungForm(forms.ModelForm):
    class Meta:
        model = Verwaltung
        fields = ["lizenznehmer", "software", "kostentyp", "lizenz_start", "lizenz_ende", "schulklasse", "anzahl_weitere_lizenzen"]

class LizenznehmerForm(forms.ModelForm):
    class Meta:
        model = Lizenznehmer
        fields = ["name", "schuleinheit"]

class SoftwareForm(forms.ModelForm):
    class Meta:
        model = Software
        fields = ["name", "url"]

class KostentypForm(forms.ModelForm):
    class Meta:
        model = Kostentyp
        fields = ["bezeichnung"]

class SchuleinheitForm(forms.ModelForm):
    class Meta:
        model = Schuleinheit
        fields = ["bezeichnung"]

class SchulklasseForm(forms.ModelForm):
    class Meta:
        model = Schulklasse
        fields = ["name", "anzahl_schueler"]
