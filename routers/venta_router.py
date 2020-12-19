from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from db.db_conection import get_db

from db.inventario_db   import ProductoInDB
from models.inventario_models import ProductoIn, ProductoInAdd, ProductoOut
from db.cliente_db   import ClienteInDB
from models.cliente_models import ClienteIn, ClienteOut, ClienteInCreate
from db.venta_db import VentaInDB
from models.venta_models import VentaInConsulta, VentaAdd, VentaOut ,VentaInDelete
from datetime import datetime


router = APIRouter()



@router.post("/venta/crear/")
async def crear_venta(new_venta: VentaAdd, db: Session = Depends(get_db)):
    venta_old_test= db.query(VentaInDB).filter(VentaInDB.id_producto.like('xx%')).all()
    
    id_new=1
    id_lista=[]
    if  venta_old_test !=[]: 
        for venta in venta_old_test:
            id_lista.append(venta.venta_id)
    if id_lista!=[]:
        id_new=max(id_lista)
    id_prod=new_venta.id_producto
    producto_in_db = db.query(ProductoInDB).get(id_prod)
    nom_pr=producto_in_db.nombre
    precio=producto_in_db.precio
    subtotal_new = new_venta.cantidad_producto *precio
    fecha=datetime.utcnow()
    obs=new_venta.observaciones
    venta_in_db = VentaInDB(**new_venta.dict(),sub_total=subtotal_new,venta_id=id_new, fecha_venta=fecha,nombre_producto=nom_pr, precio_producto=precio)
    db.add(venta_in_db)
    db.commit()
    db.refresh(venta_in_db)
    carrito=db.query(VentaInDB).filter((VentaInDB.venta_id==id_new )).filter(~VentaInDB.id_producto.like('xx%')).all()
    return carrito



@router.get("/venta/comprar/",response_model=VentaOut)
async def comprar_venta( db: Session = Depends(get_db)):
    
    venta_old_test= db.query(VentaInDB).filter(VentaInDB.id_producto.like('xx%')).all()
    if  venta_old_test!=[]: 
        for venta in venta_old_test:
            db.delete(venta)
            db.commit()
    

    ventas_totales = db.query(VentaInDB).all()
    ids=0
    id_lista=[]
    for venta in ventas_totales:
        id_lista.append(venta.venta_id)
    if  id_lista!=[]:
        ids=max(id_lista)    

    venta_prueba={
    "venta_id":          ids+1,
    "id_producto":       "xx00",
    "nombre_producto":   "prueba",
    "precio_producto":   0,
    "cantidad_producto": 0,
    "sub_total":0,
    "fecha_venta":       datetime.utcnow(),
    "telefono":          3137878599,
    "observaciones":    ""
    }

    venta_in_db=VentaInDB(**venta_prueba)
    db.add(venta_in_db)
    db.commit()
    db.refresh(venta_in_db)
    return venta_in_db

@router.get("/venta/lista/")
async def listar(db: Session = Depends(get_db)):
    prueba= db.query(VentaInDB).filter(VentaInDB.id_producto.like('xx%')).one()
    lista = db.query(VentaInDB).filter(VentaInDB.id_producto!=prueba.id_producto).all()
    return lista    


@router.delete("/venta/eliminar/")
async def venta_elimiar(del_venta: VentaInDelete, db: Session = Depends(get_db)):
    venta_to_del = db.query(VentaInDB).get([del_venta.venta_id,del_venta.id_producto,del_venta.telefono])
    db.delete(venta_to_del)
    db.commit()
    
    return "se eliminó del carrito"    

@router.get("/venta/carrito/")
async def crear_venta(db: Session = Depends(get_db)):
    venta_old_test= db.query(VentaInDB).filter(VentaInDB.id_producto.like('xx%')).all()
    id_new=1
    id_lista=[]
    if  venta_old_test !=[]: 
        for venta in venta_old_test:
            id_lista.append(venta.venta_id)
    if id_lista!=[]:
        id_new=max(id_lista)
    carrito=db.query(VentaInDB).filter((VentaInDB.venta_id==id_new )).filter(~VentaInDB.id_producto.like('xx%')).all()
    return carrito