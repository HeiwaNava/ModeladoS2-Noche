#la conexion a la base de datos y el manejo de la misma
#MySQL usando SQLAlchemy como nuestro ORM ( Object-Relational Mapping )
# convierte tablas de mysql a clases de python

#3 conceptos clave:
#1. Engine: representa la conexión fisica al motor de la base de datos
#2. Sesion: Unidad de trabajo que acumla operaciones antes de enviarlas a la DB
#3. Base: Clase padre de la cual heredan todos los modelos del ORM

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Cargar las varuavkes definidas en el archivo .env al entorno del proceso

load_dotenv()
# esta evita tener que escribir las variables directamente
DATABASE_URL = (f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME')}")

# creamos el Engine
engine = create_engine(DATABASE_URL,pool_pre_ping=True)

# creamos la sesion
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# declaramos la base
# heredar todos lode modelos del ORM
class Base(DeclarativeBase):
    pass

#utilizamos un generador para obtener una sesion de DB a cada enpoint de fasapi
#get_db

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()