from django.db import models


class Schuleinheit(models.Model):
    bezeichnung = models.CharField(max_length=100)

    def __str__(self):
        return self.bezeichnung


class Lizenznehmer(models.Model):
    name = models.CharField(max_length=100)
    schuleinheit = models.ForeignKey(Schuleinheit, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Software(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class Kostentyp(models.Model):
    bezeichnung = models.CharField(max_length=100)

    def __str__(self):
        return self.bezeichnung


class Schulklasse(models.Model):
    name = models.CharField(max_length=100)
    anzahl_schueler = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Verwaltung(models.Model):
    lizenznehmer = models.ForeignKey(Lizenznehmer, on_delete=models.CASCADE)
    software = models.ForeignKey(Software, on_delete=models.CASCADE)
    kostentyp = models.ForeignKey(Kostentyp, on_delete=models.CASCADE)
    lizenz_start = models.DateField()
    lizenz_ende = models.DateField()
    schulklasse = models.ForeignKey(
        Schulklasse,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    anzahl_weitere_lizenzen = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.lizenznehmer} - {self.software}"
