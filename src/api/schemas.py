#DTO de pydantic 

#son como los contratos del API
#define exactamente que datos se esperan en cada peticion y que datos se devuelven como respuesta


from typing import Optional
from pydantic import BaseModel

#ROL
class RolCreate(BaseModel):
    nombre_rol:str

class RolResponse(BaseModel):
    id_rol: int
    nombre_rol: str
    model_config = {'from_attributes':True}

#Usuario

class UsuarioCreate(BaseModel):
    id_rol: int
    nombre_completo: str
    correo: str
    contraseña_hash: str

class UsuarioResponse(BaseModel):
    id_rol: int
    id_usuario: int
    nombre_completo: str
    correo: str
    model_config = {'from_attributes': True}

class UsuarioUpdate(BaseModel):
    id_rol: Optional[int] = None
    nombre_completo: Optional[str] = None
    correo: Optional[str] = None
    contraseña_hash: Optional[str] = None