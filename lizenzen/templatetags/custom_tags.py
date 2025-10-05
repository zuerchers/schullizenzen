from django import template

register = template.Library()

@register.filter
def getattr_value(obj, field_name):
    """
    Holt dynamisch ein Feld vom Objekt.
    - Gibt bei FK-Objekten automatisch 'bezeichnung' oder 'name' zurück (falls vorhanden),
      sonst das Objekt selbst.
    - Fällt auf '' zurück, wenn das Attribut fehlt oder None ist.
    """
    val = getattr(obj, field_name, "")
    if val is None:
        return ""
    # Für FK-Objekte einen hübschen String wählen
    if hasattr(val, "bezeichnung"):
        return val.bezeichnung
    if hasattr(val, "name"):
        return val.name
    return val
