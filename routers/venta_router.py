from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from db.db_conection import get_db

from db.inventario_db   import ProductoInDB
from models.inventario_models import ProductoIn, ProductoInAdd, ProductoOut
from db.cliente_db   import ClienteInDB
from models.cliente_models import ClienteIn, ClienteOut, ClienteInCreate
from db.venta_db import VentaInDB
from models.venta_models import VentaInConsulta, VentaAdd, VentaOut


router = APIRouter()



@router.post("/venta/crear/",response_model=VentaOut)
async def crear_venta(new_venta: VentaAdd, db: Session = Depends(get_db)):
    '''
     id_producto_new = new_venta.id_producto
     cant_producto_new = new_venta.cantidad_producto
     nombre_producto_new = new_venta.nombre_producto
     precio_producto_new = new_venta.precio_producto
     telefono_producto_new = new_venta.telefono
     
     venta_id_new = new_venta.venta_id
    '''
    subtotal_new = new_venta.cantidad_producto * new_venta.precio_producto
    venta_in_db = VentaInDB(**new_venta.dict(),sub_total=subtotal_new)
    db.add(venta_in_db)
    db.commit()
    db.refresh(venta_in_db)
    return venta_in_db






'''


@api.put("/transaccion/make/")
async def make_transaccion(new_transaccion: TransaccionIn):
    #venta_new = new_transaccion.venta_id
    #if id == None:        
    #  raise HTTPException(status_code=404, detail="El producto no existe")
    
    #Para agregarle el id de venta automáticamente
    ventas = get_all_ventas()
    #Elige el id de la última venta
    venta = ventas[len(ventas)-1]

    productos = get_all_productos_dict()
    producto = productos[len(productos)-1]
    precio = producto["precio"]
   
    subtotal = new_transaccion.cant_pedido * precio

    transaccion_ingresar = TransaccionInDB(**new_transaccion.dict(), venta_id=venta["venta_id"],tran_subtotal=subtotal )
    #transaccion_ingresar = TransaccionInDB(**new_transaccion.dict(), venta_id=new_transaccion.transaccion_id)
    transaccion_in_db = save_transaccion(transaccion_ingresar)
    transaccion_out=TransaccionOut(**transaccion_in_db.dict())
    return  transaccion_out
'''