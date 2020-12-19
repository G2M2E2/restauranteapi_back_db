from sqlalchemy import Column, Integer, String, Date, BigInteger, ForeignKey, DateTime
from db.db_conection import Base, engine
import datetime


class VentaInDB(Base):
    __tablename__ = "venta"
    venta_id          = Column(Integer, primary_key=True)
    id_producto       = Column(String, ForeignKey('producto.id_producto'), primary_key=True) ###entrada
    nombre_producto   = Column(String) ##Estas variables son para busqueda en inventario y agregar al carrito
    precio_producto   = Column(BigInteger) ##Estas variables son para busqueda en inventario y agregar al carrito
    sub_total         = Column(BigInteger) ##Calculo cantidad * precio
    cantidad_producto = Column(Integer) ## entradas
    fecha_venta       = Column(DateTime, default=datetime.datetime.utcnow)
    observaciones     = Column(String)
    telefono          = Column(BigInteger, ForeignKey('cliente.telefono'), primary_key=True) ##Estas variables son para busqueda en clientes y agregar en carrito


Base.metadata.create_all(bind=engine)  






'''
from typing import Dict
from datetime import datetime
from pydantic import BaseModel



class VentaInDB(BaseModel):
    venta_id: int = 0
    venta_fecha: datetime = datetime.now()
    venta_total: int
    telefono: int
    username: str

def get_all_ventas():
    return database_ventas


database_ventas = []
generator = {"id":0}


def save_venta(ventas_in_db: VentaInDB):
    generator["id"] = generator["id"] + 1
    ventas_in_db.venta_id = generator["id"]
    database_ventas.append(ventas_in_db)
    return ventas_in_db


def get_venta(id: int):
    if ((id-1) < len(database_ventas)):
        return database_ventas[id-1]
    else:
        return "No existe la factura buscada"
'''        