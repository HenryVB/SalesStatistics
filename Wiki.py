import streamlit as st
from PIL import Image

# Streamlit de presentación, con titulo y resumen de proyecto

st.set_page_config(
    page_title="Aplicacion de Ventas",
    page_icon=":chart_with_upwards_trend:"
)

st.title("Análisis de Ventas")

st.write("""
Este proyecto tiene como objetivo analizar los datos de ventas de SOAINT para comprender tendencias de las oportunidades que permitan al equipo comercial potenciar la fuerza de ventas.\n
Se realizó el proceso de limpieza y transformación de los datos iniciales. \n
En la pestaña Dashboard Se muestran los datos generales y graficas para reflejar los Key Performance Indicators (KPIs) o insights
que permiten la evaluación del comportamiento de clientes, identificar tendencias y toma de decisiones en base a ello.
""")

image = Image.open("data/sales.jpg")
st.image(image, use_column_width=True)

st.header("Datos Generales")

st.write("""
- **Valor 1: Total de Ventas:** Representa el valor total de las ventas generadas.

- **Valor 2: Promedio por Venta Ganada:** Representa el valor promedio de cada venta exitosa.

- **Valor 3: Tasa de Conversión:** Indica el porcentaje de oportunidades que resultan en ventas exitosas.

- **Valor 4: Tasa de Cancelación:** Indica el porcentaje de oportunidades que no se han podido convertir en exitosas.
""")

st.header("Graficos")

st.write("""
- **Grafico 1: Distribución de Probabilidades:** Este gráfico permite identificar tendencias de oportunidades y ajustar estrategias de venta.

- **Grafico 2: Rendimiento por Propietario de Negocio:** Este gráfico permite evaluar el rendimiento del personal en terminos monetarios, a fin de identificar aquellos que están debajo o por encima del umbral.

- **Grafico 3: Impacto de Probabilidad en el Valor de la divisa:** Este gráfico permite ver cual(es) categoría(s) se asocian con los valores monetarios más altos.

- **Gráfico 4: Análisis Temporal de Oportunidades:** Esta métrica visualiza la cantidad de oportunidades a lo largo del tiempo.
""")
