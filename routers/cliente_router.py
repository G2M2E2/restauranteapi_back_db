from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session


from db.db_conection import get_db
from db.cliente_db   import ClienteInDB
from models.cliente_models import ClienteIn, ClienteOut, ClienteInCreate


router = APIRouter()


@router.get("/cliente/consulta/{telefono}",response_model=ClienteOut)
async def get_cliente(telefono: int, db: Session = Depends(get_db)):
    
    cliente_in_db = db.query(ClienteInDB).get(telefono)

    if cliente_in_db == None:
        raise HTTPException(status_code=404, detail="El cliente no existe")
        
    return cliente_in_db

@router.post("/cliente/crear/",response_model=ClienteOut)
async def register_cliente(cliente_in: ClienteInCreate, db: Session = Depends(get_db)):
    cliente_in_db = ClienteInDB(**cliente_in.dict())

    db.add(cliente_in_db)
    db.commit()
    db.refresh(cliente_in_db)

    return cliente_in_db

@router.post("/cliente/actualizar/",response_model=ClienteOut)
async def update_cliente(cliente_in: ClienteInCreate, db: Session = Depends(get_db)):
    
    cliente_upd = db.query(ClienteInDB).get(cliente_in.telefono)
    cliente_upd.barrio=cliente_in.barrio
    cliente_upd.cedula=cliente_in.cedula 
    cliente_upd.correo_electronico=cliente_in.correo_electronico
    cliente_upd.cumpleanos=cliente_in.cumpleanos
    cliente_upd.direccion=cliente_in.direccion
    cliente_upd.nombre=cliente_in.nombre
       
    db.commit()
    

    return cliente_upd


@router.get("/cliente/lista/")
async def buscar_clientes(db: Session = Depends(get_db)):
    clientes_in_db = db.query(ClienteInDB).all()
    return clientes_in_db

@router.delete("/cliente/eliminar/")
async def cliente_elimiar(clie_del:ClienteIn, db: Session = Depends(get_db)):
    cliente_to_del = db.query(ClienteInDB).get(clie_del.telefono)
    nombre_clien=cliente_to_del.nombre
    db.delete(cliente_to_del)
    db.commit()
    
    return "se eliminó "+ nombre_clien      



