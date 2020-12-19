from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session


from db.db_conection import get_db

from db.usuario_db         import UsuarioInDB
from models.usuario_models         import UsuarioIn, UsuarioOut


router = APIRouter()



@router.post("/usuario/auth/")
async def auth_user(user_in: UsuarioIn, db: Session = Depends(get_db)):
    
    user_in_db = db.query(UsuarioInDB).get(user_in.username)

    if user_in_db == None:
        raise HTTPException(status_code=404, detail="El usuario no existe")
    
    if user_in_db.password != user_in.password:
        raise HTTPException(status_code=403, detail="Error de autenticacion")

    return  {"Autenticado": True}




@router.post("/usuario/register/")
async def register_user(user_in: UsuarioIn, db: Session = Depends(get_db)):
    

    user_in_db = UsuarioInDB(**user_in.dict())

    db.add(user_in_db)
    db.commit()
    db.refresh(user_in_db)

    return user_in_db

    