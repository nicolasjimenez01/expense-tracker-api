from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from app.utils.settings import settings

MONGO_URL = settings.MONGO_URL

try:
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    # Verificar la conexión
    client.admin.command('ping')
    print("✓ Conexión exitosa a MongoDB")
    
    db = client["expense-tracker"]
    users_collection = db["user"]
    expenses_collection = db["expenses"]

    users_collection.create_index("username", unique=True)
    users_collection.create_index("email", unique=True)
    
except ConnectionFailure as e:
    print(f"✗ Error al conectar a MongoDB: {e}")
    print("Asegúrate de que MongoDB esté corriendo en localhost:27017")
    raise
except Exception as e:
    print(f"✗ Error inesperado: {e}")
    raise