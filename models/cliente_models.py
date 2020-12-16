from pydantic import BaseModel
from datetime import date

class ClienteIn(BaseModel):
    telefono: int

class ClienteInCreate(BaseModel):
    telefono: int
    nombre: str
    direccion: str
    barrio: str
    cedula: str
    cumpleanos: str
    correo_electronico: str

class ClienteOut(BaseModel):
    telefono: int
    nombre: str
    direccion: str
    barrio: str
    cedula: str
    cumpleanos: str
    correo_electronico: str
    class Config:
        orm_mode = True


