# db/conexion.py

from pymongo import MongoClient
from configuracion import MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION

# Crear el cliente y conectar
cliente = MongoClient(MONGO_URI)

# Seleccionar la base de datos
db = cliente[MONGO_DB_NAME]

# Seleccionar la colección
coleccion_viviendas = db[MONGO_COLLECTION]

# Mensaje opcional de éxito
print(" Conectado a MongoDB:", MONGO_URI)
print(f" Base de datos: {MONGO_DB_NAME}, Colección: {MONGO_COLLECTION}")