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

# ==============================================================================

# Modificaciones realizadas por Emilio Suarez (Dev 2)
# Nota para Dev 3: He agregado todas las excepciones del dominio. Ya puedes iniciar la clase abstracta base y la entidad Cliente.

# ==============================================================================

class InvalidClientError(SoftwareFJError):
  """Lanzada cuando un cliente contiene datos con formato incorrecto."""

  def __init__(self, detalle):
    super().__init__(f"Error de Datos de Cliente: {detalle}")


class ServiceUnavailableError(SoftwareFJError):
  """Lanzada cuando se intenta usar un servicio inactivo o deshabilitado."""

  def __init__(self, nombre_servicio):
    super().__init__(
        f"Servicio No Disponible: El servicio '{nombre_servicio}' está fuera de"
        " servicio."
    )


class ReservationError(SoftwareFJError):
  """Lanzada ante fallos en la confirmación o cancelación de reservas."""

  def __init__(self, id_reserva, motivo):
    super().__init__(f"Error en Reserva [{id_reserva}]: {motivo}")


class CalculationError(SoftwareFJError):
  """Lanzada ante incoherencias matemáticas en duraciones o tarifas."""

  def __init__(self, detalle):
    super().__init__(f"Error de Cálculo: {detalle}")


