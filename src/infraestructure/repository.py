#los crud

#el repositorio encapsula las consultas SQL
#solo sabe como guardar, recuperar, eliminar y modificar los datos
#pero no sabe porque

from typing import Optional, List, Type, TypeVar
from sqlalchemy.orm import Session
from src.domain.models import (Roles, Usuario, Estudiante, Profesor, Monitor)

#se usa para que el tipo de retorno de los archivos genericos sea consistente
#con el modelo (roles, usuario, estudiantes, etc)
T = TypeVar("T")

#clase base con las operaciones genericas del CRUD
#Insert, Select, Delete, Updater

class BaseRepository:
    def __init__(self, model:Type, db: Session):
        #model: es la clase del ORM (Rol, Usuario, Estudiante, Etc)
        #db: la sesion de conexion a la base de datos
        self.model = model
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List:
        #offset: salta los primeros N registros, util para la paginacion de los datos
        #limit: devuelve como maximo N registros
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    def get_by_id(self, record_id: int) -> Optional: #si no encuentra el ID retorna None
        pk = self.model.__mapper__.primary_key[0].name
        return self.db.query(self.model).filter(getattr(self.model, pk)== record_id).first()
    
    def create(self, obj) -> object:
        self.db.add(obj) #añadir el objeto a la sesion, aun no esta en la base de datos
        self.db.commit() #enviamos el insert a la DB y se confirma
        self.db.refresh(obj) #recargamos el objeto desde la base de datos
        return obj
    
    def update(self, obj) -> object:
        self.db.commit() #enviamos el update a la DB y se confirma
        self.db.refresh(obj) #recargamos el objeto desde la base de datos
        return obj
    
    def delete(self,recor_id: int) -> bool:
        obj = self.get_by_id(recor_id)
        if not obj:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True
    
class RolRepository(BaseRepository):
    def __init__(self, db:Session):
        super().__init__(Roles, db)

    def get_by_nombre(self, nombre:str) -> Optional[Roles]:
        return self.db.query(Roles).filter(Roles.nombre_rol == nombre).first()
    
class UsuarioRepository(BaseRepository):
    def __init__(self, db:Session):
        super().__init__(Usuario, db)

    def get_by_nombre(self, nombre:str) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.nombre_completo == nombre).first()
    
    def get_by_correo(self, correo:str) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.correo == correo).first()

    
