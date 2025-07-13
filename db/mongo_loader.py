# db/mongo_loader.py

from pymongo import MongoClient
from configuracion import MONGO_URI, MONGO_DB_NAME, TIPOS_COLL, VIVIENDAS_COLL
from dataset.cargar_guardar import leer_datos_excel

def poblar_tipos(df):
    """
    Inserta los tipos únicos de vivienda en la colección TIPOS_COLL.
    Devuelve un dict mapping tipo → ObjectId.
    """
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB_NAME]
    coll_tipos = db[TIPOS_COLL]
    # Reinicia la colección para no duplicar
    coll_tipos.drop()

    tipos_unicos = df['tipo'].unique().tolist()
    docs = [{'nombre': t} for t in tipos_unicos]
    result = coll_tipos.insert_many(docs)

    # Crear mapping tipo → ObjectId
    mapping = {
        tipo: oid
        for tipo, oid in zip(tipos_unicos, result.inserted_ids)
    }
    print(f"Poblados {len(tipos_unicos)} tipos en '{TIPOS_COLL}'")
    return mapping

def poblar_viviendas(df, tipo_mapping):
    """
    Inserta cada vivienda en VIVIENDAS_COLL, referenciando el tipo por su ObjectId.
    """
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB_NAME]
    coll_viv = db[VIVIENDAS_COLL]
    coll_viv.drop()

    registros = []
    for _, row in df.iterrows():
        registros.append({
            'precio':       float(row['precio']),
            'area':         float(row['area']),
            'habitaciones': int(row['habitaciones']),
            'antiguedad':   int(row['antiguedad']),
            'fecha_publicacion': row['fecha_publicacion'],  # datetime si ya lo convertiste
            'descripcion':  row['descripcion'],
            'tipo_id':      tipo_mapping[row['tipo']],
        })
    if registros:
        coll_viv.insert_many(registros)
    print(f"Pobladas {len(registros)} viviendas en '{VIVIENDAS_COLL}'")

def cargar_a_mongo():
    """
    Flujo completo para limpiar, extraer tipos y cargar todo en MongoDB.
    """
    # 1. Leer y limpiar el DataFrame
    df = leer_datos_excel()

    # 2. Insertar tipos y obtener mapping
    mapping = poblar_tipos(df)

    # 3. Insertar viviendas referenciando tipos
    poblar_viviendas(df, mapping)

if __name__ == "__main__":
    cargar_a_mongo()
    print("✅ Carga completa a MongoDB.")
