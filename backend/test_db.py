# test_db.py
from sqlalchemy import text
from app.core.database import engine

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("✅ Conexão com SiHealth realizada com sucesso!")
except Exception as e:
    print(f"❌ Erro ao conectar: {e}")