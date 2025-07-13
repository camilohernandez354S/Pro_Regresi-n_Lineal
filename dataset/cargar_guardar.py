# dataset/cargar_guardar.py

import os
import pandas as pd
from configuracion import EXCEL_PATH
from db.conexion import coleccion_viviendas

def leer_datos_excel() -> pd.DataFrame:
    """
    Lee el archivo Excel con los datos de viviendas y devuelve un DataFrame
    con las columnas originales más:
      - precio_m2: precio dividido por área
      - tipo_vivienda: 'Casa', 'Apartamento' u 'Otro'
      - tipo: misma info que tipo_vivienda, para normalización en Mongo
    """
    if not os.path.exists(EXCEL_PATH):
        raise FileNotFoundError(f"No se encontró el archivo: {EXCEL_PATH}")
    
    
    # Carga los datos
    df = pd.read_excel(EXCEL_PATH, header=0, engine='openpyxl')
    
    # --- Limpieza inicial de descripciones mal codificadas ---
    replacements = {
        'Apartamento cÃ©ntrico': 'Apartamento céntrico',
        'Apartamento econÃ³mico': 'Apartamento económico',
        'Casa con jardÃ­n':     'Casa con jardín',
        # añade aquí más casos según aparezcan…
    }
    df['descripcion'] = df['descripcion'].replace(replacements)
    # ---------------------------------------------------------
    
    # Calcula precio por m²
    df['precio_m2'] = df['precio'] / df['area']
    
    # Clasifica el tipo de vivienda
    def _clasificar(desc):
        txt = desc.lower() if isinstance(desc, str) else ""
        if 'casa' in txt:
            return 'Casa'
        if 'apartamento' in txt:
            return 'Apartamento'
        return 'Otro'
    
    df['tipo_vivienda'] = df['descripcion'].apply(_clasificar)
    # Añadimos columna 'tipo' para el loader de normalización en MongoDB
    df['tipo'] = df['tipo_vivienda']
    
    return df

def insertar_en_mongo(reemplazar: bool = True) -> int:
    """
    Lee el DataFrame y lo inserta en MongoDB (coleccion_viviendas).
    Si reemplazar=True, primero borra todos los documentos existentes.
    Devuelve la cantidad de documentos insertados.
    """
    df = leer_datos_excel()
    registros = df.to_dict(orient='records')
    
    if reemplazar:
        coleccion_viviendas.delete_many({})
    
    result = coleccion_viviendas.insert_many(registros)
    return len(result.inserted_ids)
