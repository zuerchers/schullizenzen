from django import template

register = template.Library()

@register.filter(name="getattr")
def getattr_filter(obj, attr_name):
    """
    Zugriff auf ein beliebiges Attribut eines Objekts.
    Beispiel: {{ obj|getattr:"feldname" }}
    """
    try:
        return getattr(obj, attr_name, "")
    except Exception:
        return ""


@register.filter(name="getattr_value")
def getattr_value(obj, field_name):
    """
    Holt dynamisch ein Feld und gibt es benutzerfreundlich aus.
    Zeigt bei FK-Objekten automatisch den Namen oder die Bezeichnung an.
    """
    try:
        val = getattr(obj, field_name, "")
        if val is None:
            return ""
        if hasattr(val, "bezeichnung"):
            return val.bezeichnung
        if hasattr(val, "name"):
            return val.name
        return str(val)
    except Exception:
        return ""
