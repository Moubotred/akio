# app/exceptions.py

class AppException(Exception):
    """Excepción lanzada cuando ocurre un rechazo o timeout en las reglas de la APK."""
    def __init__(self, mensaje_usuario: str, categoria: int = 0):
        self.mensaje_usuario = mensaje_usuario
        self.categoria = categoria