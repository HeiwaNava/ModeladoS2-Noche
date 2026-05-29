#casos de uso del sistema
#Los servicios contienen la logica del negocio
#saben que hacer, pero le delegan a los repositorios como hacer el CRU

#responsabilidad de esta capa
#orquestar la comunicacion con los repositorios
#aplicar las reglas de negocio (ej: una reserva de un laboratorio, solo se aprueba si esta en estado pendiente)
#trasformar los datos antes de retornarlos al API

#Capa API = Recibir las peticiones HTTP
#Servicio = aplica la logica del negocio
#Repositorio = Ejecuta las consultas SQL CRUD
#Infraestructura = no es conocida por el API

from typing import List, Optional
from sqlalchemy.orm import Session

from src.domain.models import Usuario, Roles
from src.infraestructure.repository import (
    UsuarioRepository,
    RolRepository
)


# ======================
# ROL SERVICE
# ======================

class RolService:
    def __init__(self, db: Session):
        self.repo = RolRepository(db)

    def listar(self) -> List[Roles]:
        return self.repo.get_all()

    def obtener(self, id_rol: int) -> Optional[Roles]:
        return self.repo.get_by_id(id_rol)

    def crear(self, nombre_rol: str) -> Roles:
        nuevo_rol = Roles(nombre_rol=nombre_rol)
        return self.repo.create(nuevo_rol)

    def eliminar(self, id_rol: int) -> bool:
        return self.repo.delete(id_rol)

# ======================
# USUARIO SERVICE
# ======================

class UsuarioService:
    def __init__(self, db: Session):
        self.repo = UsuarioRepository(db)

    def listar(self) -> List[Usuario]:
        return self.repo.get_all()

    def obtener(self, id_usuario: int) -> Optional[Usuario]:
        return self.repo.get_by_id(id_usuario)

    def obtenerNombre(self, nombre_usuario: str) -> Optional[Usuario]:
        return self.repo.get_by_nombre(nombre_usuario)

    def obtenerCorreo(self, correo: str) -> Optional[Usuario]:
        return self.repo.get_by_correo(correo)

    def crear(
        self,
        id_rol: int,
        nombre_completo: str,
        correo: str,
        contrasena_hash: str
    ) -> Usuario:

        nuevo_usuario = Usuario(
            id_rol=id_rol,
            nombre_completo=nombre_completo,
            correo=correo,
            contrasena_hash=contrasena_hash
        )

        return self.repo.create(nuevo_usuario)

    def eliminar(self, id_usuario: int) -> bool:
        return self.repo.delete(id_usuario)

    def actualizar(
        self,
        id_usuario: int,
        **kwargs
    ) -> Optional[Usuario]:

        usuario = self.repo.get_by_id(id_usuario)

        if not usuario:
            return None

        for key, value in kwargs.items():
            setattr(usuario, key, value)

        return self.repo.update(usuario)