from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from db.db_conection import get_db
from db.inventario_db   import ProductoInDB
from models.inventario_models import ProductoIn, ProductoInAdd, ProductoOut ,ProductoInDelete


router = APIRouter()


@router.get("/producto/consulta/{id_producto}",response_model=ProductoOut)
async def get_producto(id_producto: str, db: Session = Depends(get_db)):
    
    producto_in_db = db.query(ProductoInDB).get(id_producto)

    if producto_in_db == None:
        raise HTTPException(status_code=404, detail="El producto no existe")
        
    return producto_in_db

@router.post("/producto/crear/",response_model=ProductoOut)
async def register_prodcutos(new_producto: ProductoInAdd, db: Session = Depends(get_db)):
    cat_new=new_producto.categoria
    productos_in_db = db.query(ProductoInDB).all()
    id_actual=cat_new[:2]+'00'
    num_list=[]
    for producto in productos_in_db:
        if cat_new==producto.categoria:
            id_actual=producto.id_producto
            num_list.append(int(id_actual[2:]))
        print(num_list)
        cat=id_actual[:2]
        num=max(num_list) 
    if num<9:
        id_new=cat+'0'+str(num+1)
    else:
        id_new=cat+str(num+1)
    producto_in_db = ProductoInDB(**new_producto.dict(),id_producto=id_new)
    db.add(producto_in_db)
    db.commit()
    db.refresh(producto_in_db)
    return producto_in_db


@router.get("/producto/lista/")
async def buscar_productos(db: Session = Depends(get_db)):
    busqueda = db.query(ProductoInDB).all()
      
    return busqueda

@router.get("/producto/consulta_n/{snombre}")
async def get_producto(snombre: str, db: Session = Depends(get_db)):
    producto=snombre+"%"
    producto_in_db = db.query(ProductoInDB).filter(ProductoInDB.nombre.like(producto)).all()

    if producto_in_db == None:
        raise HTTPException(status_code=404, detail="El producto no existe")

    print(producto_in_db[0].categoria)   
    return producto_in_db

@router.put("/producto/actualizar/",response_model=ProductoOut)
async def update_cliente(producto_in: ProductoOut, db: Session = Depends(get_db)):
    
    producto_upd = db.query(ProductoInDB).get(producto_in.id_producto)
    producto_upd.nombre=producto_in.nombre
    producto_upd.precio=producto_in.precio 
    producto_upd.cantidad=producto_in.cantidad
    producto_upd.categoria=producto_in.categoria
    db.commit()
    return producto_upd   


@router.get("/producto/consulta_g/{scategoria}")
async def get_producto(scategoria: str, db: Session = Depends(get_db)):
    producto=scategoria+"%"
    producto_in_db = db.query(ProductoInDB).filter(ProductoInDB.categoria.like(producto)).all()

    if producto_in_db == None:
        raise HTTPException(status_code=404, detail="El producto no existe")

    print(producto_in_db[0].categoria)   
    return producto_in_db

@router.delete("/producto/eliminar/")
async def producto_elimiar(prod_del:ProductoInDelete, db: Session = Depends(get_db)):
    producto_to_del = db.query(ProductoInDB).get(prod_del.id_producto)
    nombre_pro=producto_to_del.nombre
    db.delete(producto_to_del)
    db.commit()
    
    return "se eliminó "+ nombre_pro     