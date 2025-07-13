# controller/grafico_dispersion.py

import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
from configuracion import EXCEL_PATH, BASE_DIR

def generar_dispersion():
    """
    Genera un diagrama de dispersión Precio vs Precio por m²,
    ajusta una regresión lineal simple y lo guarda como 'static/grafico.png'.
    """
    # 1. Leer y limpiar datos (leer_datos_excel ya corrige descripciones y extrae tipo)
    df = pd.read_excel(EXCEL_PATH, engine='openpyxl')
    df['precio_m2'] = df['precio'] / df['area']

    # 2. Scatter de los datos
    plt.figure(figsize=(10, 6))
    plt.scatter(df['precio'], df['precio_m2'], alpha=0.6, edgecolors='k', label='Datos reales')

    # 3. Ajuste de regresión lineal simple
    X = df[['precio']].values.reshape(-1, 1)
    y = df['precio_m2'].values
    modelo = LinearRegression().fit(X, y)

    # 4. Línea de regresión
    x_line = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
    y_line = modelo.predict(x_line)
    plt.plot(x_line, y_line, 'r-', linewidth=2, label='Línea de regresión')

    # 5. Decoración
    plt.title("Precio vs Precio por m² con Línea de Regresión")
    plt.xlabel("Precio de la Vivienda")
    plt.ylabel("Precio por m²")
    plt.legend()
    plt.grid(True)

    # 6. Guardar en static/grafico.png
    ruta_img = os.path.join(BASE_DIR, 'static', 'grafico.png')
    os.makedirs(os.path.dirname(ruta_img), exist_ok=True)
    plt.savefig(ruta_img, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"Gráfico con regresión guardado en {ruta_img}")
