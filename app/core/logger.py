import os
import logging
from logging.handlers import RotatingFileHandler

# Definir el formato de los logs
LOG_FORMAT = "%(levelname)s: \t  %(filename)s:%(lineno)d %(message)s"

# Lee la variable de entorno APP_LOG_LEVEL (por defecto usa DEBUG)
log_level_env = os.getenv("APP_LOG_LEVEL", "DEBUG").upper()

# Convierte el string 'DEBUG' o 'INFO' al nivel correspondiente de logging
LOG_LEVEL = getattr(logging, log_level_env, logging.DEBUG)

# Handler para escribir en archivo con rotación (máx 5MB por archivo, conserva 3 respaldos)
file_handler = RotatingFileHandler(
    "app.log", maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# Handler para ver los logs en la consola
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# Configuración global de logging
logging.basicConfig(
    level=logging.DEBUG,  # Cambiar a logging.INFO en producción
    handlers=[file_handler, console_handler]
)

LIBRERIAS_A_SILENCIAR = [
    # "uvicorn",
    "aiosqlite",
    # "uvicorn.access",  # Quita los logs de cada petición HTTP en consola
    # "uvicorn.error",
    "asyncio",
    "urllib3",
    "requests",
    "sqlalchemy.engine",  # Silencia las consultas SQL si usas SQLAlchemy
    "httpcore",
    "httpcore.connection",
    "httpcore.http11",
    "httpx",

]

for lib in LIBRERIAS_A_SILENCIAR:
    # Solo mostrará WARNING o ERROR (ignora DEBUG e INFO)
    logging.getLogger(lib).setLevel(logging.WARNING)

# Función helper para obtener loggers nombrados por módulo
def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)