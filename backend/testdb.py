from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def test():
    uri = os.getenv("MONGO_URI")
    client = AsyncIOMotorClient(uri)
    try:
        await client.admin.command("ping")
        print("✅ Conexão com MongoDB Atlas bem-sucedida!")
    except Exception as e:
        print("❌ Erro ao conectar:", e)

asyncio.run(test())
