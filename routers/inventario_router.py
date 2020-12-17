from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from db.db_conection import get_db
from db.inventario_db   import ProductoInDB
from models.inventario_models import ProductoIn, ProductoInAdd, ProductoOut


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
    for producto in productos_in_db:
        if cat_new==producto.categoria:
            id_actual=producto.id_producto
    cat=id_actual[:2]
    num=int(id_actual[2:])
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


@router.get("/producto/consulta_g/{scategoria}")
async def get_producto(scategoria: str, db: Session = Depends(get_db)):
    producto=scategoria+"%"
    producto_in_db = db.query(ProductoInDB).filter(ProductoInDB.categoria.like(producto)).all()

    if producto_in_db == None:
        raise HTTPException(status_code=404, detail="El producto no existe")

    print(producto_in_db[0].categoria)   
    return producto_in_db    