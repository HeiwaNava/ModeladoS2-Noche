#capa de dominio

from datetime import datetime
from typing import Optional, List
from sqlalchemy import Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

#importamos la clase base desde 
from src.infraestructure.database import Base

#=================
# ROL
#=================

class Roles(Base):
    __tablename__ = "ROLES"
    #primary key
    #auto incremental
    id_rol: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True)
    nombre_rol:Mapped[str] = mapped_column(String(50))
    
    #Relacion inversa: Desde rol podemos acceder a la lista de usuarios
    usuarios:Mapped[List["Usuario"]] = relationship(back_populates="rol")


class Usuario(Base):
    __tablename__ = "USUARIOS"

    id_usuario: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    id_rol: Mapped[int] = mapped_column(ForeignKey("ROLES.id_rol"))

    nombre_completo: Mapped[str] = mapped_column(String(150))
    correo: Mapped[str] = mapped_column()
    contrasena_hash: Mapped[str] = mapped_column(String(253))

    rol: Mapped["Roles"] = relationship(back_populates="usuarios")

    estudiante: Mapped[Optional["Estudiante"]] = relationship(back_populates="usuario",uselist=False)
    profesor: Mapped[Optional["Profesor"]] = relationship(back_populates="usuario",uselist=False)
    monitor: Mapped[Optional["Monitor"]] = relationship(back_populates="usuario",uselist=False)


class Estudiante(Base):
    __tablename__ = "ESTUDIANTES"
#al ser pk y fk al mismo tiempo, en este caso se vincula al estudiante con el usuario
    id_usuario: Mapped[int] = mapped_column(ForeignKey("USUARIOS.id_usuario"), primary_key=True)
    matricula: Mapped[str] = mapped_column(String(50), unique=True)
    programa: Mapped[str] = mapped_column(String(100))
    
    usuario: Mapped["Usuario"] = relationship(back_populates="estudiante")


class Profesor(Base):
    __tablename__ = "PROFESORES"
    #al ser pk y fk al mismo tiempo, en este caso se vincula al profesor con el usuario
    id_usuario: Mapped[int] = mapped_column(ForeignKey("USUARIOS.id_usuario"), primary_key=True)
    departamento: Mapped[str] = mapped_column(String(100))

    usuario: Mapped["Usuario"] = relationship(back_populates="profesor")

class Monitor(Base):
    __tablename__ = "MONITORES"
     #al ser pk y fk al mismo tiempo, en este caso se vincula al monitor con el usuario
    id_usuario: Mapped[int] = mapped_column(ForeignKey("USUARIOS.id_usuario"), primary_key=True)
    id_turno: Mapped[int] = mapped_column(Integer)
    
    usuario: Mapped["Usuario"] = relationship(back_populates="monitor")
#monitor gestiona las reservas
#monitor tiene que ver con los prestamos


#Recurso
  #Laboratorio
  #Equipos_Portatiles
  #Reservas
  #Novedades

class Recursos(Base):
    __tablename__ = "RECURSOS"
    id_recurso: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_placa: Mapped[str] = mapped_column(ForeignKey("PLACAS.id_placa"))
    
    Recursos : Mapped["Laboratorios"] = relationship(back_populates="Recursos")
    

    
class Reservas(Base):
    __tablename__ = "RESERVAS"
    id_reserva: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_usuario_solicita: Mapped[int] = mapped_column(ForeignKey("RESERVAS.id_usuario_solicita"))
    id_recurso : Mapped[int] = mapped_column(ForeignKey("RESERVAS.id_recurso"))
    id_monitor_aprueba : Mapped[int] = mapped_column(ForeignKey("RESERVAS.id_monitor_aprueba"))
    fecha_inicio : Mapped[DateTime] = mapped_column(DateTime)
    fecha_fin : Mapped[DateTime] = mapped_column(DateTime)
    estado : Mapped[str] = mapped_column(String(50))
    proposito : Mapped[str] = mapped_column(String(255))
    
    reservas: Mapped[List["Reservas"]] = relationship(back_populates="recurso")
    
class Equipos_portatiles(Base):
    __tablename__= "EQUIPOS_PORTATILES"
    id_recurso : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    modelo : Mapped[str] = mapped_column(String(100))
    sistema_operativo : Mapped[str] = mapped_column(String(50))
    
class Laboratorios(Base):
    __tablename__= "LABORATORIOS"
    id_recurso : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    capacidad : Mapped[int] = mapped_column(Integer)
    software : Mapped[str] = mapped_column(String(255))
    ubicacion : Mapped[str] = mapped_column(String(100))
    
class Prestamos(Base):
    __tablename__= "PRESTAMOS"
    id_prestamo : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_reserva : Mapped[int] = mapped_column(ForeignKey("RESERVAS.id_reserva"))
    id_monitor_entrega : Mapped[int] = mapped_column(ForeignKey("MONITORES.id_monitor_entrega"))
    hora_entrega : Mapped[DateTime] = mapped_column(DateTime)
    hora_devolucion : Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    estado_recepcion : Mapped[str] = mapped_column(String(50),  nullable=True)
    
class Sanciones(Base):
    __tablename__= "SANCIONES"
    id_sancion : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_usuario_estudiante : Mapped[int] = mapped_column(ForeignKey("SANCIONES.id_usuario_estudiante"))
    id_prestamo : Mapped[int] = mapped_column(ForeignKey("SANCIONES.id_prestamo"))
    fecha_inicio : Mapped[DateTime] = mapped_column(DateTime)
    fecha_fin : Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    motivo : Mapped[str] = mapped_column(String(255))
    estado : Mapped[str] = mapped_column(String(50))