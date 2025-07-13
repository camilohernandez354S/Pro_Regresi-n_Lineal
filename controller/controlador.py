# controller/controlador.py

from flask import Flask, render_template
from dataset.cargar_guardar import leer_datos_excel
from controller.generación_grafico import generar_dispersion
from configuracion import DEBUG

import os
from configuracion import BASE_DIR

# Ahora Flask sabrá exactamente dónde están tus plantillas y estáticos
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)


def clasificar(desc):
    """Devuelve tipo de vivienda según la descripción."""
    if not isinstance(desc, str):
        return 'Otro'
    txt = desc.lower()
    if 'casa' in txt:
        return 'Casa'
    if 'apartamento' in txt:
        return 'Apartamento'
    return 'Otro'

# controller/controlador.py (solo el método dashboard)

@app.route('/')
def dashboard():
    df = leer_datos_excel()

    # Estadísticas
    total = len(df)
    precio_promedio = df['precio'].mean()
    area_promedio = df['area'].mean()
    df['precio_m2'] = df['precio'] / df['area']
    precio_m2_promedio = df['precio_m2'].mean()
    precio_min = df['precio'].min()
    precio_max = df['precio'].max()
    area_comun = df['area'].mode()[0]

    # Conteo por tipo
    def clasificar(desc):
    # Si desc no es str, devolvemos 'Otro' inmediatamente
        if not isinstance(desc, str):
            return 'Otro'
        txt = desc.lower()
        if 'casa' in txt:
            return 'Casa'
        if 'apartamento' in txt:
            return 'Apartamento'
        return 'Otro'

    conteo = df['descripcion'].apply(clasificar).value_counts().to_dict()

    # Tabla HTML
    tabla_html = df.to_html(classes='table table-bordered', index=False)

    return render_template(
        'dashboard.html',
        total_viviendas=total,
        precio_promedio=f"{precio_promedio:,.0f}",
        area_promedio=f"{area_promedio:,.0f}",
        precio_m2_promedio=f"{precio_m2_promedio:,.0f}",
        casas_count=conteo.get('Casa', 0),
        apartamentos_count=conteo.get('Apartamento', 0),
        otros_count=conteo.get('Otro', 0),
        precio_min=f"{precio_min:,.0f}",
        precio_max=f"{precio_max:,.0f}",
        area_comun=f"{area_comun:,.0f}",
        tabla=tabla_html,
        ruta_grafico='grafico.png'
    )


@app.route('/tabla')
def mostrar_tabla():
    df = leer_datos_excel()
    tabla_html = df.to_html(classes='table table-striped', index=False)
    return render_template('tabla_datos.html', tabla=tabla_html)

@app.route('/resumen')
def resumen():
    df = leer_datos_excel()
    df['precio_m2'] = df['precio'] / df['area']
    df['descripcion'] = df['descripcion'].fillna('')
    total = len(df)
    promedio_m2 = round(df['precio_m2'].mean(), 2)
    conteo = df['descripcion'].apply(clasificar).value_counts().to_dict()
    return render_template(
        'resumen_estadistico.html',
        total=total,
        promedio_m2=promedio_m2,
        conteo=conteo
    )

@app.route('/grafico')
def grafico():
    generar_dispersion()
    return render_template('grafico_dispersion.html')
