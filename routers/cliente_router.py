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


@router.get("/cliente/lista/")
async def buscar_clientes(db: Session = Depends(get_db)):
    clientes_in_db = db.query(ClienteInDB).all()
    return clientes_in_db



