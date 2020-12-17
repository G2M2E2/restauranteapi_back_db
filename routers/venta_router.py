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
    venta_old_test= db.query(VentaInDB).filter(VentaInDB.id_producto.like('xx%')).all()
    id_new=1
    if  venta_old_test: 
        for venta in venta_old_test:
            id_new=venta.venta_id


    subtotal_new = new_venta.cantidad_producto * new_venta.precio_producto
    venta_in_db = VentaInDB(**new_venta.dict(),sub_total=subtotal_new,venta_id=id_new)
    db.add(venta_in_db)
    db.commit()
    db.refresh(venta_in_db)
    return venta_in_db



@router.get("/venta/comprar/",response_model=VentaOut)
async def comprar_venta( db: Session = Depends(get_db)):
    
    venta_old_test= db.query(VentaInDB).filter(VentaInDB.id_producto.like('xx%')).all()
    if  venta_old_test: 
        for venta in venta_old_test:
            db.delete(venta)
            db.commit()
    

    ventas_totales = db.query(VentaInDB).all()
    ids=0
    for venta in ventas_totales:
        ids=venta.venta_id

    venta_prueba={
    "venta_id":          ids+1,
    "id_producto":       "xx00",
    "nombre_producto":   "prueba",
    "precio_producto":   0,
    "cantidad_producto": 0,
    "sub_total":0,
    "fecha_venta":       "hoy",
    "telefono":          3137878599
    }

    venta_in_db=VentaInDB(**venta_prueba)
    db.add(venta_in_db)
    db.commit()
    db.refresh(venta_in_db)
    return venta_in_db

@router.get("/venta/lista/")
async def listar(db: Session = Depends(get_db)):
    lista = db.query(VentaInDB).all()
    return lista    




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