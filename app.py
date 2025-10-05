import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

# --- Configuración Inicial de la Página ---
st.set_page_config(
    page_title="Dashboard de Ventas",
    layout="wide",
    page_icon="📊"
)

# --- 1. Generación y Caching de Datos (Reemplazo de MySQL) ---

# Usamos st.cache_data para simular la persistencia y velocidad
# de cargar los datos, tal como lo haría Streamlit con una BD.
@st.cache_data
def load_data():
    """
    Simula la obtención de datos de ventas desde una base de datos.
    Genera un DataFrame aleatorio con fechas, productos y ventas.
    """

    # 1. Definición de Parámetros
    start_date = datetime.now() - timedelta(days=90)
    dates = [start_date + timedelta(days=i) for i in range(90)]

    # Lista de productos que simula la tabla 'ventas'
    products = ['Laptop Pro', 'Monitor 4K', 'Tablet', 'Auriculares BT', 'Cargador Inalámbrico']

    # Creación de filas de datos
    data = []
    for date in dates:
        # Generamos entre 10 y 30 transacciones por día
        num_transactions = np.random.randint(10, 30)
        for _ in range(num_transactions):
            data.append({
                'fecha': date,
                'producto': np.random.choice(products),
                'ventas': np.random.randint(50, 1500) # Monto de venta aleatorio
            })

    df = pd.DataFrame(data)

    # Aseguramos que 'fecha' sea tipo datetime para el gráfico
    df['fecha'] = pd.to_datetime(df['fecha'])

    return df

# --- 2. Lógica de Filtros (Barra Lateral) ---

def create_sidebar(df):
    """
    Crea la barra lateral de control y aplica los filtros al DataFrame.
    """
    with st.sidebar:
        st.title("Controles de Filtro")

        # Filtro de Producto (Multiselect)
        all_products = df['producto'].unique()
        producto_seleccionado = st.multiselect(
            "Filtrar Producto",
            options=all_products,
            default=all_products # Por defecto, selecciona todos
        )

        # Filtro de Fecha (Rango de Fechas)
        min_date = df['fecha'].min().date()
        max_date = df['fecha'].max().date()

        date_range = st.date_input(
            "Seleccionar Rango de Fechas",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

    df_filtrado = df.copy()

    # Aplicar Filtro de Producto
    if producto_seleccionado:
        df_filtrado = df_filtrado[df_filtrado['producto'].isin(producto_seleccionado)]

    # Aplicar Filtro de Fecha (si se seleccionan ambas fechas)
    if len(date_range) == 2:
        start, end = date_range
        # Convertir a datetime para la comparación
        df_filtrado = df_filtrado[
            (df_filtrado['fecha'].dt.date >= start) &
            (df_filtrado['fecha'].dt.date <= end)
            ]

    # Mostrar la cantidad de registros filtrados para referencia
    st.sidebar.info(f"Registros filtrados: {len(df_filtrado)}")

    return df_filtrado

# --- 3. Despliegue de Métricas ---

def display_metrics(df):
    """
    Calcula y muestra las tres métricas principales en columnas.
    """
    col1, col2, col3 = st.columns(3)

    # Cálculo simple de crecimiento (simulado para mantener el ejemplo del video)
    crecimiento_venta = 12.5
    crecimiento_productos = 3
    crecimiento_promedio = 8.2

    # Métrica 1: Ventas Totales
    with col1:
        total_venta = df['ventas'].sum()
        st.metric(
            "Ventas Totales",
            f"${total_venta:,.0f}",
            f"{crecimiento_venta}%" # Simula el delta
        )

    # Métrica 2: Productos Activos (Únicos)
    with col2:
        productos_unicos = df['producto'].nunique()
        st.metric(
            "Productos Activos",
            productos_unicos,
            f"+{crecimiento_productos}"
        )

    # Métrica 3: Promedio de Venta
    with col3:
        promedio_venta = df['ventas'].mean()
        st.metric(
            "Promedio Diario",
            f"${promedio_venta:,.0f}",
            f"{crecimiento_promedio}%"
        )

# --- 4. Despliegue de Gráficos y Tabla ---

def display_charts(df):
    """
    Crea y muestra los gráficos y la tabla de datos en la disposición final.
    """

    # 4.1 Gráficos en Columnas
    st.markdown("---") # Separador visual
    col_chart1, col_chart2 = st.columns(2)

    # Gráfico 1: Tendencia de Ventas (Línea)
    with col_chart1:
        st.subheader("Tendencia de Ventas (Línea)")

        # Agrupamos las ventas por día para la tendencia
        df_tendencia = df.groupby('fecha')['ventas'].sum().reset_index()

        fig_lineas = px.line(
            data_frame=df_tendencia,
            x='fecha',
            y='ventas',
            title='Ventas Diarias',
            template='plotly_dark'
        )
        fig_lineas.update_layout(height=400)
        st.plotly_chart(fig_lineas, use_container_width=True)

    # Gráfico 2: Ventas por Producto (Barras)
    with col_chart2:
        st.subheader("Ventas por Producto (Barras)")

        # Agrupar y sumar las ventas por producto
        ventas_por_producto = df.groupby('producto')['ventas'].sum().reset_index()

        fig_barras = px.bar(
            data_frame=ventas_por_producto,
            x='producto',
            y='ventas',
            title='Ventas Agrupadas por Artículo',
            template='plotly_dark'
        )
        st.plotly_chart(fig_barras, use_container_width=True)

    # 4.2 Expander para la Tabla
    st.markdown("---")
    with st.expander("Ver datos detallados de la tabla"):
        st.dataframe(df, use_container_width=True)


# --- 5. Función Principal del Dashboard ---

def main():
    """
    Ejecuta el flujo completo de la aplicación Streamlit.
    """
    st.title("📊 Dashboard de Ventas Profesional con Streamlit")
    st.markdown("Bienvenido. Este dashboard simula la carga de datos de ventas para mostrar métricas y gráficos interactivos.")

    # 1. Cargar datos (simulados)
    df_original = load_data()

    # 2. Crear barra lateral y obtener datos filtrados
    df_filtrado = create_sidebar(df_original)

    # 3. Mostrar las métricas
    display_metrics(df_filtrado)

    # 4. Mostrar gráficos y tabla
    display_charts(df_filtrado)

if __name__ == '__main__':
    main()
