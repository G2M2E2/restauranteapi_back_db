
from fastapi import Depends, FastAPI

from routers.cliente_router  import router as router_clientes 
from routers.inventario_router  import router as router_productos 
from routers.venta_router import router as router_ventas
from routers.usuario_router import router as router_usuarios

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
origins = [
"http://localhost.tiangolo.com", "https://localhost.tiangolo.com",
"http://localhost", "http://localhost:8080","https://restaurante-front.herokuapp.com",
"https://restaurante-front-db.herokuapp.com",
]
app.add_middleware(
CORSMiddleware, allow_origins=origins,
allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)
app.include_router(router_clientes)
app.include_router(router_productos)
app.include_router(router_ventas)
app.include_router(router_usuarios)

'''
from db.usuario_db import UsuarioInDB
from db.usuario_db import update_usuario, get_usuario
from models.usuario_models import UsuarioIn, UsuarioOut
from db.cliente_db import ClienteInDB
from db.cliente_db import update_cliente, get_cliente, create_cliente, eliminate_cliente, get_all_clientes
from models.cliente_models import ClienteIn, ClienteOut, ClienteInCreate
from db.inventario_db import ProductoInDB
from db.inventario_db import update_producto, get_producto, create_producto, delete_producto, get_all_productos
from models.inventario_models import ProductoIn, ProductoOut, ProductoInCreate,ProductoInAdd
from models.venta_models import VentaIn, VentaOut
from db.venta_db import VentaInDB, get_all_ventas,save_venta,get_venta

from datetime import datetime

from fastapi import FastAPI
from fastapi import HTTPException

api = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
origins = [
"http://localhost.tiangolo.com", "https://localhost.tiangolo.com",
"http://localhost", "http://localhost:8080","https://restaurante-front.herokuapp.com",
]
api.add_middleware(
CORSMiddleware, allow_origins=origins,
allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

@api.post("/usuario/autenticacion/")
async def auth_user(user_in: UsuarioIn):
    user_in_db =get_usuario(user_in.username)
    if user_in_db == None:
        raise HTTPException(status_code=404,
                            detail="El usuario no existe")
    if user_in_db.password != user_in.password:
        raise HTTPException(status_code=401, detail="Error en la autenticación")
    return {"Autenticado": True}

@api.post("/usuario/crear/") 
async def create_user(user_in: UsuarioIn):
    user_in_db=update_usuario(user_in)
    user_out = UsuarioOut(**user_in_db.dict())
    user_new = get_usuario(user_out.username)
    if user_new == None:
        raise HTTPException(status_code=404,detail="El usuario no ha sido creado")
    return {"Creado": True}

@api.get("/cliente/consulta/{telefono}")
async def buscar_cliente(telefono: int):
    cliente_in_db = get_cliente(telefono)
    if cliente_in_db == None:
        raise HTTPException(status_code=404,
                            detail="El cliente no existe")
    cliente_out = ClienteOut(**cliente_in_db.dict())
    return cliente_out   

@api.get("/cliente/lista/")
async def buscar_clientes():
    clientes_in_db = get_all_clientes()
    clientes_out = []
    for cliente in clientes_in_db:
        cliente_out = ClienteOut(**cliente.dict())
        clientes_out.append(cliente_out)
    return clientes_out

@api.post("/cliente/crear/") 
async def crear_cliente(cliente_in: ClienteInCreate):
    cliente_in_db = create_cliente(cliente_in)
    cliente_out = ClienteOut(**cliente_in_db.dict())
    return cliente_out

@api.put("/cliente/update/")
async def upd_cliente(cliente_in: ClienteInCreate):
    cliente_in_db = get_cliente(cliente_in.telefono)
    if cliente_in_db == None:
        raise HTTPException(status_code=404,
                            detail="El cliente no existe")
    
    cliente_in_db = ClienteInCreate(**cliente_in.dict())

    update_cliente(cliente_in_db)
    
    update_out = ClienteOut(**cliente_in_db.dict())
    return update_out

@api.delete("/cliente/delete/") 

async def delete_cliente(cliente_in: ClienteIn):
    cliente_in_db = get_cliente(cliente_in.telefono)
    if cliente_in_db == None:
        raise HTTPException(status_code=404,
                            detail="El cliente no existe")
    cliente_out = eliminate_cliente(cliente_in_db)
    return cliente_out

#####Inventario

@api.post("/producto/crear/")
def add_producto(new_producto:ProductoInAdd):
    cat_new=new_producto.categoria
    productos_in_db = get_all_productos()
    for producto in productos_in_db:
        if cat_new==producto.categoria:
            id_actual=producto.id
    cat=id_actual[:2]
    num=int(id_actual[2:])
    if num<9:
        id_new=cat+'0'+str(num+1)
    else:
        id_new=cat+str(num+1)
    producto_ingresar = ProductoInDB(**new_producto.dict(),id=id_new)
    producto_in_db=create_producto(producto_ingresar)
    producto_out = ProductoOut(**producto_in_db.dict())
    return producto_out

@api.get("/producto/consulta/{id}")
async def buscar_producto(id: str):
    producto_in_db = get_producto(id)
    if producto_in_db == None:
        raise HTTPException(status_code=404,
                            detail="El producto no existe")
    producto_out = ProductoOut(**producto_in_db.dict())
    return producto_out  

@api.get("/producto/lista/")
async def buscar_productos():
    productos_in_db = get_all_productos()
    productos_out = []
    for producto in productos_in_db:
        producto_out = ProductoOut(**producto.dict())
        productos_out.append(producto_out)
    return productos_out

@api.put("/producto/update/")
async def update_producto(producto_in: ProductoInCreate):
    producto_in_db = get_producto(producto_in.id)
    if producto_in_db == None:
        raise HTTPException(status_code=404,
                            detail="El producto no existe")
    
    producto_in_db = ProductoInCreate(**producto_in.dict())

    update_producto(producto_in_db)
    
    update_out = ProductoOut(**producto_in_db.dict())
    return update_out

@api.delete("/producto/delete/") 

async def delete_producto(producto_in: ProductoIn):
    producto_in_db = get_producto(producto_in.id)
    if producto_in_db == None:
        raise HTTPException(status_code=404,
                            detail="El producto no existe")
    producto_out = delete_producto(producto_in_db)
    return producto_out

@api.get("/venta/list/")
async def lista_ventas():
    ventas_in_db = get_all_ventas()
    ventas_out = []
    for venta in ventas_in_db:
        venta_out = VentaOut(**venta.dict())
        ventas_out.append(venta_out)
    return ventas_out


@api.put("/venta/make/")
async def make_venta(venta_in: VentaIn):
    
    user_in_db = get_usuario(venta_in.username)

    if user_in_db == None:        
        raise HTTPException(status_code=404, detail="El usuario no tiene permisos para hacer ventas")
    ### venta_total = acá tendría en cuenta la cantidad de productos y precio del producto para saber el precio total de acuerdo a inventario
    ventas_in_db = VentaInDB(**venta_in.dict())
    ventas_in_db.venta_fecha = datetime.now()
    ventas_in_db = save_venta(ventas_in_db)
    venta_out = VentaOut(**ventas_in_db.dict())

    return  venta_out    

@api.get("/venta/consulta/{id}")
async def buscar_venta(id: int):
    venta_in_db = get_venta(id)
    return venta_in_db


"""@api.get("/venta/consulta/{telefono}")
async def buscar_venta(telefono: int):
    venta_in_db = get_venta(telefono)
    if venta_in_db == None:
        raise HTTPException(status_code=404, detail="no tiene ventas")
    return venta_in_db"""

   '''
