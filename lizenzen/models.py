from django.db import models


# ========================
#  BASISMODELLE (FK-Listen)
# ========================

class Schuleinheit(models.Model):
    bezeichnung = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["bezeichnung"]
        verbose_name = "Schuleinheit"
        verbose_name_plural = "Schuleinheiten"

    def __str__(self):
        return self.bezeichnung


class Schulklasse(models.Model):
    name = models.CharField(max_length=50)
    anzahl_schueler = models.PositiveIntegerField(default=0, blank=True, null=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Schulklasse"
        verbose_name_plural = "Schulklassen"

    def __str__(self):
        count = self.anzahl_schueler or 0
        return f"{self.name} ({count} SuS)"


class Kostentyp(models.Model):
    bezeichnung = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["bezeichnung"]
        verbose_name = "Kostentyp"
        verbose_name_plural = "Kostentypen"

    def __str__(self):
        return self.bezeichnung


class Software(models.Model):
    name = models.CharField(max_length=100, unique=True)
    url = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Software"
        verbose_name_plural = "Software"

    def __str__(self):
        return self.name


class Lizenznehmer(models.Model):
    name = models.CharField(max_length=100)
    schuleinheit = models.ForeignKey(
        Schuleinheit,
        on_delete=models.SET_NULL,   # ← falls Einheit gelöscht wird, bleibt Lizenznehmer erhalten
        null=True,                   # ← darf in DB NULL sein
        blank=True,                  # ← darf in Formularen leer bleiben
        related_name="lizenznehmer"
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Lizenznehmer"
        verbose_name_plural = "Lizenznehmer"

    def __str__(self):
        if self.schuleinheit:
            return f"{self.name} ({self.schuleinheit.bezeichnung})"
        return self.name


# ========================
#  HAUPTTABELLE (MASTER)
# ========================

class Verwaltung(models.Model):
    lizenznehmer = models.ForeignKey(Lizenznehmer, on_delete=models.CASCADE)
    software = models.ForeignKey(Software, on_delete=models.CASCADE)
    kostentyp = models.ForeignKey(Kostentyp, on_delete=models.CASCADE)
    schulklasse = models.ForeignKey(
        Schulklasse,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    lizenz_start = models.DateField()
    lizenz_ende = models.DateField()
    anzahl_weitere_lizenzen = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["lizenznehmer", "software"]
        verbose_name = "Lizenzverwaltung"
        verbose_name_plural = "Lizenzverwaltungen"

    def __str__(self):
        return f"{self.lizenznehmer} → {self.software}"
