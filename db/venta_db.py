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