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

# ==============================================================================
# 4. VALIDACIÓN DE EMAIL Y TELEFONO (ENCAPSULACION DE CLIENTE)
# Autor: Auri Paez (Dev 4)
# Nota para Dev 5: Cliente queda 100% validado con excepciones. Te paso el testigo para crear la clase abstracta Servicio.
# ==============================================================================

    @property
    def email(self):
      return self._email

    @email.setter
    def email(self, valor):
      valor_str = str(valor).strip()
      if "@" not in valor_str or "." not in valor_str:
        raise InvalidClientError(
            f"El correo '{valor_str}' no es un email válido."
        )
      self._email = valor_str

    @property
    def telefono(self):
      return self._telefono

    @telefono.setter
    def telefono(self, valor):
      valor_str = str(valor).strip()
      if len(valor_str) < 7:
        raise InvalidClientError("El teléfono debe tener al menos 7 dígitos.")
      self._telefono = valor_str

    def obtener_identificador(self):
      return self._id_cliente

    def __str__(self):
      return f"Cliente [{self._id_cliente}]: {self._nombre} ({self._email})"

# ==============================================================================
# 4. SERVICIOS Y POLIMORFISMO
# Autor: Aura Moreno (Dev 5)
# Nota para Dev 1: Definí el contrato abstracto de Servicio. Por favor crea la primera subclase ReservaSala.
# ==============================================================================


class Servicio(EntidadSistema):
  """Clase abstracta para los servicios ofertados por Software FJ."""

  def __init__(self, cod_servicio, nombre_servicio, precio_base):
    self.cod_servicio = cod_servicio
    self.nombre_servicio = nombre_servicio
    self.precio_base = float(precio_base)
    self.disponible = True

  def obtener_identificador(self):
    return self.cod_servicio

  def validar_disponibilidad(self):
    if not self.disponible:
      raise ServiceUnavailableError(self.nombre_servicio)

  @abstractmethod
  def calcular_costo(self, duracion, impuesto=0.19, descuento=0.0):
    pass

  @abstractmethod
  def describir(self):
    pass

# Modificaciones realizadas por Jesus Martinez (Dev 1)
# Nota para Dev 2: ReservaSala terminada. Continúa con la subclase AlquilerEquipo.


class ReservaSala(Servicio):
  """Subclase para la reserva de salas de reuniones/conferencias."""

  def __init__(
      self,
      cod_servicio,
      nombre_servicio,
      precio_hora,
      capacidad_personas,
      incluye_proyector=True,
  ):
    super().__init__(cod_servicio, nombre_servicio, precio_hora)
    self.capacidad_personas = int(capacidad_personas)
    self.incluye_proyector = incluye_proyector

  def calcular_costo(self, duracion, impuesto=0.19, descuento=0.0):
    if duracion <= 0:
      raise CalculationError("La duración en horas debe ser mayor a 0.")
    subtotal = self.precio_base * duracion
    if self.incluye_proyector:
      subtotal += 50000.0  # Cargo adicional por proyector
    subtotal_desc = subtotal * (1.0 - descuento)
    return round(subtotal_desc * (1.0 + impuesto), 2)

  def describir(self):
    proy = "Con proyector" if self.incluye_proyector else "Sin proyector"
    return (
        f"Sala '{self.nombre_servicio}' (Capacidad: {self.capacidad_personas}"
        f" pers, {proy}) - ${self.precio_base:,.0f}/h"
    )
# Modificaciones realizadas por Emilio Suarez (Dev 2)
# Nota para Dev 3: AlquilerEquipo lista. Falta la tercera subclase AsesoriaEspecializada.


class AlquilerEquipo(Servicio):
  """Subclase para el alquiler de equipos de cómputo."""

  def __init__(
      self,
      cod_servicio,
      nombre_servicio,
      precio_dia,
      tipo_equipo,
      deposito_garantia=100000.0,
  ):
    super().__init__(cod_servicio, nombre_servicio, precio_dia)
    self.tipo_equipo = tipo_equipo
    self.deposito_garantia = float(deposito_garantia)

  def calcular_costo(self, duracion, impuesto=0.19, descuento=0.0):
    if duracion <= 0:
      raise CalculationError("La duración en días debe ser mayor a 0.")
    subtotal = (self.precio_base * duracion) * (1.0 - descuento)
    return round((subtotal * (1.0 + impuesto)) + self.deposito_garantia, 2)

  def describir(self):
    return (
        f"Equipo '{self.nombre_servicio}' [{self.tipo_equipo}] -"
        f" ${self.precio_base:,.0f}/día (Garantía:"
        f" ${self.deposito_garantia:,.0f})"
    )


# Modificaciones realizadas por Bryam Garizabal (Dev 3)
# Nota para Dev 4: Catálogo de servicios completado. Inicia el modelo Reserva.


class AsesoriaEspecializada(Servicio):
  """Subclase para consultorías especializadas en software."""

  def __init__(
      self,
      cod_servicio,
      nombre_servicio,
      precio_hora,
      consultor,
      nivel_experiencia="Senior",
  ):
    # Llama al constructor de Servicio (código, nombre y precio base por hora)
    super().__init__(cod_servicio, nombre_servicio, precio_hora)
    # Atributos propios de la asesoría
    self.consultor = consultor
    self.nivel_experiencia = nivel_experiencia

  def calcular_costo(self, duracion, impuesto=0.19, descuento=0.0):
    # Una duración de 0 o negativa no tiene sentido: error de cálculo propio
    if duracion <= 0:
      raise CalculationError("La duración debe ser mayor a 0 horas.")
    # Los consultores Senior cobran un 30% más; los demás, tarifa normal
    mult = 1.3 if self.nivel_experiencia == "Senior" else 1.0
    # Subtotal = tarifa x horas x multiplicador, menos el descuento
    subtotal = (self.precio_base * duracion * mult) * (1.0 - descuento)
    # Se suma el impuesto y se redondea a 2 decimales
    return round(subtotal * (1.0 + impuesto), 2)

  def describir(self):
    # Devuelve un texto que resume la asesoría (polimorfismo de describir)
    return (
        f"Asesoría '{self.nombre_servicio}' con {self.consultor}"
        f" ({self.nivel_experiencia}) - ${self.precio_base:,.0f}/h"
    )

# ==============================================================================
# 5. GESTIÓN DE RESERVAS (ESTRUCTURA TRY / EXCEPT / ELSE / FINALLY)
# Autor: Auri paez (Dev 4)
# Nota para Dev 5: Creé la base de la clase Reserva. Favor implementar confirmar_reserva() con bloque try/except/else/finally.
# ==============================================================================


class Reserva(EntidadSistema):
  """Gestiona el ciclo de vida de una reserva con control estricto de excepciones."""

  def __init__(self, id_reserva, cliente, servicio, duracion):
    self.id_reserva = id_reserva
    self.cliente = cliente
    self.servicio = servicio
    self.duracion = duracion
    self.estado = "PENDIENTE"

  def obtener_identificador(self):
    return self.id_reserva


    # Modificaciones realizadas por Aura Moreno (Dev 5)
    # Nota para Dev 1: Método confirmar_reserva listo. Por favor agrega cancelar_reserva() y los métodos de cálculo.

    def confirmar_reserva(self):
      logger.info(f"Procesando confirmación de reserva [{self.id_reserva}]...")
      try:
        if self.estado != "PENDIENTE":
          raise ReservationError(
              self.id_reserva,
              f"La reserva ya se encuentra en estado '{self.estado}'.",
          )
        self.servicio.validar_disponibilidad()
      except ServiceUnavailableError as err:
        logger.error(f"Error confirmando reserva [{self.id_reserva}]: {err}")
        self.estado = "RECHAZADA"
        raise ReservationError(
            self.id_reserva, "Servicio inactivo."
        ) from err
      except ReservationError as err:
        logger.warning(f"Advertencia en reserva [{self.id_reserva}]: {err}")
        raise
      else:
        self.estado = "CONFIRMADA"
        logger.info(f"Reserva [{self.id_reserva}] CONFIRMADA exitosamente.")
      finally:
        logger.debug(
            f"Fin del procesamiento para reserva [{self.id_reserva}]. Estado"
            f" final: {self.estado}"
        )

    # Modificaciones realizadas por Jesus Martinez (Dev 1)
    # Nota para Dev 2: La clase Reserva está completa. Te dejo la creación del script de simulación de las 10 operaciones.

    def cancelar_reserva(self):
      try:
        if self.estado == "CANCELADA":
          raise ValueError("La reserva ya estaba cancelada anteriormente.")
        self.estado = "CANCELADA"
        logger.info(f"Reserva [{self.id_reserva}] CANCELADA por el cliente.")
      except ValueError as err:
        logger.error(f"Error cancelando reserva [{self.id_reserva}]: {err}")
        raise ReservationError(
            self.id_reserva, "Acción inválida."
        ) from err

    def calcular_total_reserva(self, impuesto=0.19, descuento=0.0):
      return self.servicio.calcular_costo(
          self.duracion, impuesto=impuesto, descuento=descuento
      )

    def __str__(self):
      return (
          f"Reserva [{self.id_reserva}] | {self.cliente.nombre} |"
          f" {self.servicio.nombre_servicio} | Estado: {self.estado}"
      )
# ==============================================================================
# 6. SIMULACIÓN DE 10 OPERACIONES SECUENCIALES
# Autor: Emilio Suarez (Dev 4)
# Nota final: Integración final de pruebas. Demuestra la captura sin caídas del sistema.
# ==============================================================================


def ejecutar_simulacion():
  print("\n" + "=" * 75)
  print("      SISTEMA DE GESTIÓN SOFTWARE FJ - SIMULACIÓN DE 10 OPERACIONES")
  print("=" * 75 + "\n")

  # OP 1: Registro correcto de Cliente 1
  print("[OP 1] Registrando Cliente Válido 1...")
  try:
    c1 = Cliente(
        "1010123456", "Carlos Pérez", "carlos.perez@email.com", "3001234567"
    )
    print(f"  -> Éxito: {c1}")
  except SoftwareFJError as e:
    print(f"  -> Error capturado: {e}")

  # OP 2: Registro fallido de Cliente (ID no numérico)
  print("\n[OP 2] Probando registro de cliente con ID inválido...")
  try:
    c_invalid = Cliente(
        "1010ABC", "Ana Gómez", "ana.gomez@email.com", "3009876543"
    )
  except SoftwareFJError as e:
    print(f"  -> Captura de Excepción Esperada: {e}")

  # OP 3: Registro fallido de Cliente (Email sin @)
  print("\n[OP 3] Probando registro de cliente con correo inválido...")
  try:
    c_invalid2 = Cliente(
        "1020304050", "Luis Torres", "correo_invalido.com", "3115551234"
    )
  except SoftwareFJError as e:
    print(f"  -> Captura de Excepción Esperada: {e}")

  # OP 4: Registro correcto de Cliente 2
  print("\n[OP 4] Registrando Cliente Válido 2...")
  try:
    c2 = Cliente("1030405060", "Laura Martínez", "laura.m@email.com", "3158889900")
    print(f"  -> Éxito: {c2}")
  except SoftwareFJError as e:
    print(f"  -> Error capturado: {e}")

  # OP 5: Creación del catálogo de servicios
  print("\n[OP 5] Creando catálogo de servicios...")
  sala1 = ReservaSala(
      "SRV-01",
      "Sala Principal A",
      precio_hora=80000,
      capacidad_personas=15,
      incluye_proyector=True,
  )
  equipo1 = AlquilerEquipo(
      "SRV-02",
      "Laptop Dell XPS",
      precio_dia=120000,
      tipo_equipo="Computador Portátil",
  )
  asesoria1 = AsesoriaEspecializada(
      "SRV-03",
      "Arquitectura en la Nube",
      precio_hora=150000,
      consultor="Ing. Ramírez",
      nivel_experiencia="Senior",
  )
  print(f"  -> {sala1.describir()}")
  print(f"  -> {equipo1.describir()}")
  print(f"  -> {asesoria1.describir()}")

  # OP 6: Reserva 1 Válida (Sala) y cálculo de costo
  print(
      "\n[OP 6] Creando y confirmando Reserva 1 (Reserva de Sala por 4"
      " horas)..."
  )
  reserva1 = Reserva("RES-101", c1, sala1, duracion=4)
  try:
    reserva1.confirmar_reserva()
    costo1 = reserva1.calcular_total_reserva(impuesto=0.19, descuento=0.10)
    print(f"  -> {reserva1}")
    print(f"  -> Total con IVA (19%) y 10% Desc: ${costo1:,.2f}")
  except SoftwareFJError as e:
    print(f"  -> Error en reserva: {e}")

  # OP 7: Confirmación doble en Reserva 1 (Error de Estado)
  print("\n[OP 7] Probando confirmación doble en Reserva 1...")
  try:
    reserva1.confirmar_reserva()
  except SoftwareFJError as e:
    print(f"  -> Captura de Excepción Esperada: {e}")

  # OP 8: Reserva 2 en Servicio Inactivo (Error ServiceUnavailableError)
  print("\n[OP 8] Probando reserva de un servicio inactivo...")
  equipo1.disponible = False
  reserva2 = Reserva("RES-102", c2, equipo1, duracion=3)
  try:
    reserva2.confirmar_reserva()
  except SoftwareFJError as e:
    print(f"  -> Captura de Excepción Esperada: {e}")

  # OP 9: Reserva 3 Válida (Asesoría) y Cancelación posterior
  print(
      "\n[OP 9] Creando Reserva 3 (Asesoría), confirmando y luego cancelando..."
  )
  reserva3 = Reserva("RES-103", c2, asesoria1, duracion=2)
  try:
    reserva3.confirmar_reserva()
    costo3 = reserva3.calcular_total_reserva()
    print(f"  -> Costo Asesoría (2h Senior + IVA): ${costo3:,.2f}")
    reserva3.cancelar_reserva()
    print(f"  -> Estado tras cancelación: {reserva3.estado}")
  except SoftwareFJError as e:
    print(f"  -> Error: {e}")

  # OP 10: Doble cancelación en Reserva 3
  print("\n[OP 10] Probando doble cancelación en Reserva 3...")
  try:
    reserva3.cancelar_reserva()
  except SoftwareFJError as e:
    print(f"  -> Captura de Excepción Esperada: {e}")

  print("\n" + "=" * 75)
  print(
      "  SIMULACIÓN FINALIZADA CON ÉXITO. REVISAR EL ARCHIVO GENERADO"
      " 'software_fj.log'"
  )
  print("=" * 75 + "\n")


if __name__ == "__main__":
  ejecutar_simulacion()








