from itsdangerous import URLSafeTimedSerializer
from django.conf import settings

serializer = URLSafeTimedSerializer(settings.SECRET_KEY)

def genera_token(user):
    """Genera un token para el usuario usando el serializer de itsdangerous"""
    return serializer.dumps(user.pk, salt=settings.SECRET_KEY)

def verifica_token(token, max_age=3600):
    """Verifica un token para el usuario usando el serializer de itsdangerous"""
    try:
        id_usuario = serializer.loads(token, salt=settings.SECRET_KEY, max_age=max_age)
        return id_usuario
    except:
        return None