from pydantic import BaseModel
from datetime import datetime

'''
class VentaIn(BaseModel):
    id_producto           : str
    cantidad_producto     : int

'''


class VentaInConsulta(BaseModel):
    venta_id              : int
    id_producto           : str
    cantidad_producto     : int

class VentaAdd(BaseModel):
    
    id_producto           : str
    cantidad_producto     : int
      
    telefono              : int
    


class VentaOut(BaseModel):
    venta_id              : int
    id_producto           : str
    cantidad_producto     : int
    nombre_producto       : str
    precio_producto       : int
    telefono              : int
    sub_total             : int
    fecha_venta           : datetime


    class Config:
        orm_mode = True






'''
from pydantic import BaseModel
from datetime import datetime

class VentaIn(BaseModel):
    venta_total: int
    telefono: int
    username: str


class VentaOut(BaseModel):
    venta_id: int 
    venta_fecha: datetime = datetime.now()
    venta_total: int
    telefono: int
    username: str
    '''