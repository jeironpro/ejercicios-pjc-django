import json
import unicodedata
import re
from django import template

register = template.Library()

@register.filter
def json_a_lista(value):
    """Convierte de json a lista para que sea legible"""
    try:
        return json.loads(value)
    except Exception:
        return []
    
@register.filter
def formatear_ejemplo(texto):
    """Formatea el ejemplo para que sea legible"""
    try:
        data = json.loads(texto)
        if isinstance(data, list):
            return "\n".join(data)
        return data
    except Exception:
        return texto

@register.filter
def normalizar_cadena(texto):
    """Normaliza la cadena para que sea unico en la base de datos"""
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    texto = texto.lower()
    texto = re.sub(r'\s+', '-', texto)
    texto = re.sub(r'[^a-z0-9-]', '', texto)
    return texto