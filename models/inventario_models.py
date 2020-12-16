from pydantic import BaseModel

class ProductoIn(BaseModel):
    id_producto: str
    nombre: str


class ProductoInAdd(BaseModel):
    nombre: str
    precio: int
    cantidad: int
    categoria: str

class ProductoOut(BaseModel):
    id_producto: str
    nombre: str
    precio: int
    cantidad: int
    categoria: str
    class Config:
        orm_mode = True


    