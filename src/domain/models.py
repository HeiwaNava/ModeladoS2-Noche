#capa de dominio

from datetime import datetime
from typing import Optional, List

from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infraestructure.database import Base

# =================
# ROL
# =================

class Roles(Base):
    __tablename__ = "ROLES"

    id_rol: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    nombre_rol: Mapped[str] = mapped_column(String(50))

    usuarios: Mapped[List["Usuario"]] = relationship(
        back_populates="rol"
    )


# =================
# USUARIO
# =================

class Usuario(Base):
    __tablename__ = "USUARIOS"

    id_usuario: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    id_rol: Mapped[int] = mapped_column(
        ForeignKey("ROLES.id_rol")
    )

    nombre_completo: Mapped[str] = mapped_column(
        String(150)
    )

    correo: Mapped[str] = mapped_column(
        String(100),
        unique=True
    )

    contrasena_hash: Mapped[str] = mapped_column(
        String(255)
    )

    # Relación con Rol
    rol: Mapped["Roles"] = relationship(
        back_populates="usuarios"
    )

    # Relaciones 1 a 1
    estudiante: Mapped[Optional["Estudiante"]] = relationship(
        back_populates="usuario",
        uselist=False
    )

    profesor: Mapped[Optional["Profesor"]] = relationship(
        back_populates="usuario",
        uselist=False
    )

    monitor: Mapped[Optional["Monitor"]] = relationship(
        back_populates="usuario",
        uselist=False
    )

    reservas_solicitadas: Mapped[List["Reservas"]] = relationship(
        back_populates="usuario_solicita",
        foreign_keys="Reservas.id_usuario_solicita"
    )


# =================
# ESTUDIANTE
# =================

class Estudiante(Base):
    __tablename__ = "ESTUDIANTES"

    id_usuario: Mapped[int] = mapped_column(
        ForeignKey("USUARIOS.id_usuario"),
        primary_key=True
    )

    matricula: Mapped[str] = mapped_column(
        String(50),
        unique=True
    )

    programa: Mapped[str] = mapped_column(
        String(100)
    )

    usuario: Mapped["Usuario"] = relationship(
        back_populates="estudiante"
    )


# =================
# PROFESOR
# =================

class Profesor(Base):
    __tablename__ = "PROFESORES"

    id_usuario: Mapped[int] = mapped_column(
        ForeignKey("USUARIOS.id_usuario"),
        primary_key=True
    )

    departamento: Mapped[str] = mapped_column(
        String(100)
    )

    usuario: Mapped["Usuario"] = relationship(
        back_populates="profesor"
    )


# =================
# MONITOR
# =================

class Monitor(Base):
    __tablename__ = "MONITORES"

    id_usuario: Mapped[int] = mapped_column(
        ForeignKey("USUARIOS.id_usuario"),
        primary_key=True
    )

    id_turno: Mapped[int] = mapped_column(
        Integer
    )

    usuario: Mapped["Usuario"] = relationship(
        back_populates="monitor"
    )


# =================
# RECURSOS
# =================

class Recursos(Base):
    __tablename__ = "RECURSOS"

    id_recurso: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    tipo_recurso: Mapped[str] = mapped_column(
        String(50)
    )

    reservas: Mapped[List["Reservas"]] = relationship(
        back_populates="recurso"
    )

    laboratorio: Mapped[Optional["Laboratorios"]] = relationship(
        back_populates="recurso",
        uselist=False
    )

    equipo_portatil: Mapped[Optional["EquiposPortatiles"]] = relationship(
        back_populates="recurso",
        uselist=False
    )


# =================
# LABORATORIOS
# =================

class Laboratorios(Base):
    __tablename__ = "LABORATORIOS"

    id_recurso: Mapped[int] = mapped_column(
        ForeignKey("RECURSOS.id_recurso"),
        primary_key=True
    )

    capacidad: Mapped[int] = mapped_column(
        Integer
    )

    software: Mapped[str] = mapped_column(
        String(255)
    )

    ubicacion: Mapped[str] = mapped_column(
        String(100)
    )

    recurso: Mapped["Recursos"] = relationship(
        back_populates="laboratorio"
    )


# =================
# EQUIPOS PORTÁTILES
# =================

class EquiposPortatiles(Base):
    __tablename__ = "EQUIPOS_PORTATILES"

    id_recurso: Mapped[int] = mapped_column(
        ForeignKey("RECURSOS.id_recurso"),
        primary_key=True
    )

    modelo: Mapped[str] = mapped_column(
        String(100)
    )

    sistema_operativo: Mapped[str] = mapped_column(
        String(50)
    )

    recurso: Mapped["Recursos"] = relationship(
        back_populates="equipo_portatil"
    )


# =================
# RESERVAS
# =================

class Reservas(Base):
    __tablename__ = "RESERVAS"

    id_reserva: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    id_usuario_solicita: Mapped[int] = mapped_column(
        ForeignKey("USUARIOS.id_usuario")
    )

    id_recurso: Mapped[int] = mapped_column(
        ForeignKey("RECURSOS.id_recurso")
    )

    id_monitor_aprueba: Mapped[Optional[int]] = mapped_column(
        ForeignKey("MONITORES.id_usuario"),
        nullable=True
    )

    fecha_inicio: Mapped[datetime] = mapped_column(
        DateTime
    )

    fecha_fin: Mapped[datetime] = mapped_column(
        DateTime
    )

    estado: Mapped[str] = mapped_column(
        String(50)
    )

    proposito: Mapped[str] = mapped_column(
        String(255)
    )

    usuario_solicita: Mapped["Usuario"] = relationship(
        back_populates="reservas_solicitadas",
        foreign_keys=[id_usuario_solicita]
    )

    recurso: Mapped["Recursos"] = relationship(
        back_populates="reservas"
    )


# =================
# PRESTAMOS
# =================

class Prestamos(Base):
    __tablename__ = "PRESTAMOS"

    id_prestamo: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    id_reserva: Mapped[int] = mapped_column(
        ForeignKey("RESERVAS.id_reserva")
    )

    id_monitor_entrega: Mapped[int] = mapped_column(
        ForeignKey("MONITORES.id_usuario")
    )

    hora_entrega: Mapped[datetime] = mapped_column(
        DateTime
    )

    hora_devolucion: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True
    )

    estado_recepcion: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True
    )


# =================
# SANCIONES
# =================

class Sanciones(Base):
    __tablename__ = "SANCIONES"

    id_sancion: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    id_usuario_estudiante: Mapped[int] = mapped_column(
        ForeignKey("USUARIOS.id_usuario")
    )

    id_prestamo: Mapped[int] = mapped_column(
        ForeignKey("PRESTAMOS.id_prestamo")
    )

    fecha_inicio: Mapped[datetime] = mapped_column(
        DateTime
    )

    fecha_fin: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True
    )

    motivo: Mapped[str] = mapped_column(
        String(255)
    )

    estado: Mapped[str] = mapped_column(
        String(50)
    )