from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta
from io import BytesIO
from openpyxl import Workbook
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas

from .models import Verwaltung, Lizenznehmer, Software, Kostentyp, Schuleinheit, Schulklasse
from .forms import (
    VerwaltungForm, LizenznehmerForm, SoftwareForm,
    KostentypForm, SchuleinheitForm, SchulklasseForm
)


# =========================================================
# -------------------- HAUPTTABELLE ------------------------
# =========================================================

def verwaltung_table(request):
    verwaltungen = Verwaltung.objects.select_related(
        "lizenznehmer", "software", "kostentyp", "schulklasse", "lizenznehmer__schuleinheit"
    ).all().order_by("id")

    context = {
        "verwaltungen": verwaltungen,
        "lizenznehmer": Lizenznehmer.objects.all().order_by("name"),
        "software_list": Software.objects.all().order_by("name"),
        "kostentypen": Kostentyp.objects.all().order_by("bezeichnung"),
        "schuleinheiten": Schuleinheit.objects.all().order_by("bezeichnung"),
        "schulklassen": Schulklasse.objects.all().order_by("name"),
        "form": VerwaltungForm(),
        "lizenznehmer_form": LizenznehmerForm(),
        "software_form": SoftwareForm(),
        "kostentyp_form": KostentypForm(),
        "schuleinheit_form": SchuleinheitForm(),
        "schulklasse_form": SchulklasseForm(),
        "today": timezone.now().date(),
        "default_end": timezone.now().date() + timedelta(days=365),
    }
    return render(request, "lizenzen/verwaltung_table.html", context)


@require_POST
def verwaltung_create(request):
    form = VerwaltungForm(request.POST)
    if form.is_valid():
        v = form.save()
        return JsonResponse({"id": v.id})
    return JsonResponse({"errors": form.errors}, status=400)


@require_POST
def verwaltung_inline_update(request, pk):
    v = get_object_or_404(Verwaltung, pk=pk)

    if request.POST.get("lizenznehmer"):
        v.lizenznehmer_id = request.POST.get("lizenznehmer")
    if request.POST.get("software"):
        v.software_id = request.POST.get("software")
    if request.POST.get("kostentyp"):
        v.kostentyp_id = request.POST.get("kostentyp")
    if "schulklasse" in request.POST:
        v.schulklasse_id = request.POST.get("schulklasse") or None
    if request.POST.get("anzahl_weitere_lizenzen") is not None:
        try:
            v.anzahl_weitere_lizenzen = int(request.POST.get("anzahl_weitere_lizenzen") or 0)
        except ValueError:
            v.anzahl_weitere_lizenzen = 0
    if request.POST.get("lizenz_start"):
        v.lizenz_start = request.POST.get("lizenz_start")
    if request.POST.get("lizenz_ende"):
        v.lizenz_ende = request.POST.get("lizenz_ende")

    v.save()
    return JsonResponse({"success": True, "id": v.id})


@require_POST
def verwaltung_inline_delete(request, pk):
    v = get_object_or_404(Verwaltung, pk=pk)
    v.delete()
    return JsonResponse({"success": True})


# =========================================================
# -------------------- FK-CREATE VIEWS ---------------------
# =========================================================

@require_POST
def lizenznehmer_create(request):
    form = LizenznehmerForm(request.POST)
    if form.is_valid():
        obj = form.save()
        return JsonResponse({"id": obj.id, "name": obj.name})
    return JsonResponse({"errors": form.errors}, status=400)


@require_POST
def software_create(request):
    form = SoftwareForm(request.POST)
    if form.is_valid():
        obj = form.save()
        return JsonResponse({"id": obj.id, "name": obj.name})
    return JsonResponse({"errors": form.errors}, status=400)


@require_POST
def kostentyp_create(request):
    form = KostentypForm(request.POST)
    if form.is_valid():
        obj = form.save()
        return JsonResponse({"id": obj.id, "name": obj.bezeichnung})
    return JsonResponse({"errors": form.errors}, status=400)


@require_POST
def schuleinheit_create(request):
    form = SchuleinheitForm(request.POST)
    if form.is_valid():
        obj = form.save()
        return JsonResponse({"id": obj.id, "name": obj.bezeichnung})
    return JsonResponse({"errors": form.errors}, status=400)


@require_POST
def schulklasse_create(request):
    form = SchulklasseForm(request.POST)
    if form.is_valid():
        obj = form.save()
        return JsonResponse({"id": obj.id, "name": obj.name})
    return JsonResponse({"errors": form.errors}, status=400)


# =========================================================
# --------------------- FK-TABLES --------------------------
# =========================================================

def render_fk_table(request, queryset, title, headers, fields, form_class, create_url, model_name):
    """Hilfsfunktion für alle FK-Tabellen."""
    context = {
        "title": title,
        "headers": headers,
        "fields": fields,
        "objects": queryset,
        "form": form_class(),
        "create_url": create_url,
        "model_name": model_name,
        "schuleinheiten": Schuleinheit.objects.all().order_by("bezeichnung"),  # für Dropdowns
    }
    return render(request, "lizenzen/fk_table.html", context)


def lizenznehmer_list(request):
    return render_fk_table(
        request,
        Lizenznehmer.objects.select_related("schuleinheit").all().order_by("name"),
        title="Lizenznehmer",
        headers=["Name", "Schuleinheit"],
        fields=["name", "schuleinheit"],
        form_class=LizenznehmerForm,
        create_url="lizenznehmer_create",
        model_name="lizenznehmer"
    )


def software_list(request):
    return render_fk_table(
        request,
        Software.objects.all().order_by("name"),
        title="Software",
        headers=["Name", "URL"],
        fields=["name", "url"],
        form_class=SoftwareForm,
        create_url="software_create",
        model_name="software"
    )


def kostentyp_list(request):
    return render_fk_table(
        request,
        Kostentyp.objects.all().order_by("bezeichnung"),
        title="Kostentypen",
        headers=["Bezeichnung"],
        fields=["bezeichnung"],
        form_class=KostentypForm,
        create_url="kostentyp_create",
        model_name="kostentyp"
    )


def schuleinheit_list(request):
    return render_fk_table(
        request,
        Schuleinheit.objects.all().order_by("bezeichnung"),
        title="Schuleinheiten",
        headers=["Bezeichnung"],
        fields=["bezeichnung"],
        form_class=SchuleinheitForm,
        create_url="schuleinheit_create",
        model_name="schuleinheit"
    )


def schulklasse_list(request):
    return render_fk_table(
        request,
        Schulklasse.objects.all().order_by("name"),
        title="Schulklassen",
        headers=["Name", "Anzahl Schüler"],
        fields=["name", "anzahl_schueler"],
        form_class=SchulklasseForm,
        create_url="schulklasse_create",
        model_name="schulklasse"
    )


# =========================================================
# ------------------ INLINE UPDATE/DELETE -----------------
# =========================================================

@require_POST
def fk_inline_update(request, model, pk, fields):
    obj = get_object_or_404(model, pk=pk)
    for f in fields:
        if f in request.POST:
            setattr(obj, f, request.POST[f])
    obj.save()
    return JsonResponse({"success": True})


@require_POST
def fk_inline_delete(request, model, pk):
    obj = get_object_or_404(model, pk=pk)
    obj.delete()
    return JsonResponse({"success": True})


@require_POST
def lizenznehmer_inline_update(request, pk):
    return fk_inline_update(request, Lizenznehmer, pk, ["name", "schuleinheit"])


@require_POST
def lizenznehmer_inline_delete(request, pk):
    return fk_inline_delete(request, Lizenznehmer, pk)


@require_POST
def software_inline_update(request, pk):
    return fk_inline_update(request, Software, pk, ["name", "url"])


@require_POST
def software_inline_delete(request, pk):
    return fk_inline_delete(request, Software, pk)


@require_POST
def kostentyp_inline_update(request, pk):
    return fk_inline_update(request, Kostentyp, pk, ["bezeichnung"])


@require_POST
def kostentyp_inline_delete(request, pk):
    return fk_inline_delete(request, Kostentyp, pk)


@require_POST
def schuleinheit_inline_update(request, pk):
    return fk_inline_update(request, Schuleinheit, pk, ["bezeichnung"])


@require_POST
def schuleinheit_inline_delete(request, pk):
    return fk_inline_delete(request, Schuleinheit, pk)


@require_POST
def schulklasse_inline_update(request, pk):
    return fk_inline_update(request, Schulklasse, pk, ["name", "anzahl_schueler"])


@require_POST
def schulklasse_inline_delete(request, pk):
    return fk_inline_delete(request, Schulklasse, pk)


# =========================================================
# ----------------------- EXPORTS --------------------------
# =========================================================

# --- Verwaltung: Eigener Export ---
def verwaltung_export_xlsx(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Verwaltung"
    ws.append([
        "Lizenznehmer", "Schuleinheit", "Software", "Kostentyp",
        "Lizenz-Start", "Lizenz-Ende", "Schulklasse",
        "Anzahl Schüler", "Weitere Lizenzen"
    ])

    for v in Verwaltung.objects.select_related(
        "lizenznehmer", "software", "kostentyp", "schulklasse", "lizenznehmer__schuleinheit"
    ):
        ws.append([
            v.lizenznehmer.name if v.lizenznehmer else "",
            v.lizenznehmer.schuleinheit.bezeichnung if v.lizenznehmer and v.lizenznehmer.schuleinheit else "",
            v.software.name if v.software else "",
            v.kostentyp.bezeichnung if v.kostentyp else "",
            v.lizenz_start.strftime("%d.%m.%Y") if v.lizenz_start else "",
            v.lizenz_ende.strftime("%d.%m.%Y") if v.lizenz_ende else "",
            v.schulklasse.name if v.schulklasse else "",
            v.schulklasse.anzahl_schueler if v.schulklasse else "",
            v.anzahl_weitere_lizenzen or "",
        ])

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="verwaltung.xlsx"'
    wb.save(response)
    return response


def verwaltung_export_pdf(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(A4))
    y = 550

    p.setFont("Helvetica-Bold", 12)
    p.drawString(30, 580, "Lizenzverwaltung – Übersicht")

    p.setFont("Helvetica", 9)
    for v in Verwaltung.objects.select_related(
        "lizenznehmer", "software", "kostentyp", "schulklasse", "lizenznehmer__schuleinheit"
    ):
        line = f"{v.lizenznehmer.name if v.lizenznehmer else ''} | {v.software.name if v.software else ''} | {v.kostentyp.bezeichnung if v.kostentyp else ''}"
        p.drawString(30, y, line)
        y -= 14
        if y < 50:
            p.showPage()
            y = 550

    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="verwaltung.pdf"'
    response.write(pdf)
    return response


# --- FK-Tabellen: Gemeinsame Export-Logik ---
def fk_export_xlsx(request, model_name):
    model_map = {
        "lizenznehmer": Lizenznehmer,
        "software": Software,
        "kostentyp": Kostentyp,
        "schuleinheit": Schuleinheit,
        "schulklasse": Schulklasse,
    }

    model = model_map.get(model_name)
    if not model:
        return HttpResponse("Unbekanntes Modell", status=400)

    wb = Workbook()
    ws = wb.active
    ws.title = model_name.capitalize()

    first = model.objects.first()
    if first:
        ws.append([field.name for field in first._meta.fields])
        for obj in model.objects.all():
            ws.append([str(getattr(obj, f.name)) for f in first._meta.fields])

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = f'attachment; filename="{model_name}.xlsx"'
    wb.save(response)
    return response


def fk_export_pdf(request, model_name):
    model_map = {
        "lizenznehmer": Lizenznehmer,
        "software": Software,
        "kostentyp": Kostentyp,
        "schuleinheit": Schuleinheit,
        "schulklasse": Schulklasse,
    }

    model = model_map.get(model_name)
    if not model:
        return HttpResponse("Unbekanntes Modell", status=400)

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Helvetica-Bold", 12)
    p.drawString(30, 800, f"{model_name.capitalize()} – Übersicht")

    y = 780
    p.setFont("Helvetica", 9)
    for obj in model.objects.all():
        p.drawString(30, y, str(obj))
        y -= 14
        if y < 50:
            p.showPage()
            y = 780

    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{model_name}.pdf"'
    response.write(pdf)
    return response
