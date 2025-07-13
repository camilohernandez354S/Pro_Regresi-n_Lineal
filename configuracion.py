# configuracion.py

import os

# -----------------------
# Directorio base del proyecto
# -----------------------
# Esto detecta la carpeta donde está este archivo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# -----------------------
# Rutas a archivos de datos
# -----------------------
# Si tu Excel está dentro de una carpeta `dataset/`
EXCEL_PATH = os.path.join(BASE_DIR, 'dataset', 'dataset_vivienda.xlsx')

# Si prefieres tener el XLSX directamente en la raíz, usa:
# EXCEL_PATH = os.path.join(BASE_DIR, 'dataset_vivienda.xlsx')

# -----------------------
# Configuración de MongoDB
# -----------------------
# URI de conexión; si tu Mongo corre localmente sin autenticación:
MONGO_URI = "mongodb://localhost:27017"

# Nombre de la base de datos y colección donde guardarás/leerás datos
MONGO_DB_NAME    = "dataset"
MONGO_COLLECTION = "viviendas"
TIPOS_COLL = "tipos_vivienda"
VIVIENDAS_COLL = "viviendas"

# -----------------------
# Parámetros adicionales
# -----------------------
# Activa o desactiva el modo debug en Flask
DEBUG = True

# Puerto en el que correrá Flask (por defecto 5000)
FLASK_PORT = 5000