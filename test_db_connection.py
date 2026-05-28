import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))
from sqlalchemy import text
from infraestructure.database import engine, SessionLocal, DATABASE_URL

def test_connection():
    print(f" Intentando conectar a: {DATABASE_URL}\n")
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * from ROLES"))
            print(" Engine conectado correctamente")
            print(f"Resultado SELECT 1: {result.fetchone()}")
    except Exception as e:
        print(f" Error en engine: {e}")
        return

    print("\n Todas las pruebas pasaron. La BD está operativa.")

test_connection()