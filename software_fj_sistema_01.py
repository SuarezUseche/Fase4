"""
software_fj_sistema.py
======================
Proyecto: Sistema de Gestión de Servicios y Reservas - Software FJ
Desarrollado en equipo por 5 integrantes.
"""

from abc import ABC, abstractmethod
import logging
import sys

# ==============================================================================
# 1. CONFIGURACIÓN DEL SISTEMA DE LOGGING
# Autor: Jesús Martínez (Dev 1)
# Nota para Dev 2: Dejo configurado el logger en 'software_fj.log'. Por favor
# continua definiendo las excepciones especificas del sistema.
# ==============================================================================

logger = logging.getLogger("SoftwareFJ")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

# Salida a archivo plano
file_handler = logging.FileHandler("software_fj.log", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Salida a consola
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

if not logger.handlers:
  logger.addHandler(file_handler)
  logger.addHandler(console_handler)


# ==============================================================================
# 2. JERARQUÍA DE EXCEPCIONES PERSONALIZADAS
# ==============================================================================


class SoftwareFJError(Exception):
  """Clase base para todas las excepciones del sistema Software FJ."""

  def __init__(self, mensaje="Ha ocurrido un error en Software FJ."):
    super().__init__(mensaje)
    self.mensaje = mensaje
