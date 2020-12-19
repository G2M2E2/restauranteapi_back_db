from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Creando Motor y Conexion con la Base de Datos
SQLALCHEMY_DATABASE_URL = "postgres://fuloieuiozijtk:085e261dba0cb1b01554c7c6cdcc61ead243600e24e8f473f1711a43c4cf8ee3@ec2-34-194-198-238.compute-1.amazonaws.com:5432/dik18adq13nsl"
engine                  = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

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