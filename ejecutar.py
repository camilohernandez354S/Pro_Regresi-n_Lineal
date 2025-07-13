# ejecutar.py

from dataset.cargar_guardar import leer_datos_excel
from controller.generación_grafico import generar_dispersion
from db.mongo_loader import cargar_a_mongo

# Importamos la app de Flask
from controller.controlador import app

def main():
    # 0) Cargar y normalizar datos en MongoDB
    cargar_a_mongo()

    # 1) Leer y preparar datos
    df = leer_datos_excel()
    df['precio_m2'] = df['precio'] / df['area']

    # 2) Resumen estadístico
    total = len(df)
    promedio_m2 = df['precio_m2'].mean()

    def clasificar(desc):
        desc = desc or ''
        txt = desc.lower()
        if 'casa' in txt:
            return 'Casa'
        if 'apartamento' in txt:
            return 'Apartamento'
        return 'Otro'

    df['tipo_vivienda'] = df['descripcion'].fillna('').apply(clasificar)
    conteo = df['tipo_vivienda'].value_counts().to_dict()

    # 3) Imprimir resumen en consola
    print("\n=== RESUMEN ESTADÍSTICO ===")
    print(f"Total de viviendas: {total}")
    print(f"Precio promedio por m²: {promedio_m2:,.2f}\n")
    print("Distribución por tipo de vivienda:")
    for tipo, cnt in conteo.items():
        print(f"  - {tipo}: {cnt}")

    # 4) Generar y guardar gráfico con regresión
    generar_dispersion()
    print("\nListo: gráfico generado en static/grafico.png")

    # 5) Arrancar servidor Flask
    print("\nIniciando servidor web en http://127.0.0.1:5000")
    app.run(debug=True)

if __name__ == "__main__":
    main()
