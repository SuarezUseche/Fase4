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


# ==============================================================================
# 3. CLASES ABSTRACTAS Y CLIENTE (ENCAPSULACIÓN ESTRICTA)
# Autor: Bryam Garizabal (Dev 3)
# Nota para Dev 4: Dejo lista la abstracción general y el constructor de Cliente con validación para ID y Nombre. Falta validar email y teléfono.
# ==============================================================================


class EntidadSistema(ABC):
  """Clase abstracta base para las entidades administradas."""

  @abstractmethod
  def obtener_identificador(self):
    """Obliga a cada entidad hija a devolver su identificador único."""
    pass


class Cliente(EntidadSistema):
  """Representa un cliente con propiedades encapsuladas y validaciones estrictas."""

  def __init__(self, id_cliente, nombre, email, telefono):
    # Son atributos privados (con "_"): no se tocan directamente desde fuera
    self._id_cliente = None
    self._nombre = None
    self._email = None
    self._telefono = None

    # Al asignar con "self.xxx" se ejecutan los setters, que validan el dato
    self.id_cliente = id_cliente
    self.nombre = nombre
    self.email = email
    self.telefono = telefono
    # Si todas las validaciones pasan, se deja constancia en el registo o log
    logger.info(f"Cliente registrado: ID {self._id_cliente} - {self._nombre}")

  @property
  def id_cliente(self):
    """Getter: permite leer el ID con cliente.id_cliente."""
    return self._id_cliente

  @id_cliente.setter
  def id_cliente(self, valor):
    """Setter: valida que el ID sea solo numérico antes de guardarlo."""
    valor_str = str(valor).strip()  # Convierte a texto y quita espacios
    if not valor_str.isdigit():  # isdigit() es False si hay letras o simbolos
      raise InvalidClientError("El ID del cliente debe ser puramente numérico.")
    self._id_cliente = valor_str  # Solo se guarda si pasó la validación

  @property
  def nombre(self):
    """Getter: permite leer el nombre con cliente.nombre."""
    return self._nombre

  @nombre.setter
  def nombre(self, valor):
    """Setter: valida que el nombre tenga al menos 3 caracteres."""
    valor_str = str(valor).strip()  # Quita espacios al inicio y al final
    if len(valor_str) < 3:  # Rechaza nombres demasiado cortos
      raise InvalidClientError(
          "El nombre del cliente debe tener al menos 3 caracteres."
      )
    self._nombre = valor_str  # Se guarda solo si es válido

