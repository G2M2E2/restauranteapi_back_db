from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Creando Motor y Conexion con la Base de Datos
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:juan1234@localhost:5432/Restaurante"
engine                  = create_engine(SQLALCHEMY_DATABASE_URL)

#Creacion de la Sesion 
SessionLocal = sessionmaker(autocommit=False, 
                            autoflush=False, 
                            bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#Creando Base para la creacion de los modelos
Base = declarative_base()
Base.metadata.schema = "domicilios"