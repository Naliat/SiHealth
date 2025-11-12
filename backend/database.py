from odmantic import AIOEngine
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Carrega o arquivo .env
load_dotenv()

# Pega as variáveis
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

# Mostra no terminal (temporário, para depuração)
print("MONGO_URI:", MONGO_URI)
print("DB_NAME:", DB_NAME)

# Cria o cliente e o engine ODMantic
client = AsyncIOMotorClient(MONGO_URI)
engine = AIOEngine(client=client, database=DB_NAME)
