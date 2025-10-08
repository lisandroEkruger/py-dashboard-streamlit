import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

# --- 1. Configuración Inicial de la Página ---
st.set_page_config(
    page_title="Dashboard Pro",
    layout="wide",
    page_icon="📊"
)

# --- 2. Generación y Caching de Datos (Simulación de BD) ---

@st.cache_data
def load_data():
    """
    Simula la obtención de datos de ventas. Genera un DataFrame aleatorio
    con 180 días de datos para un cálculo de delta más robusto.
    """

    # Parámetros de la simulación
    start_date = datetime.now() - timedelta(days=180)
    dates = [start_date + timedelta(days=i) for i in range(180)]
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
                # Ventas aleatorias
                'ventas': np.random.randint(50, 5000)
            })

    df = pd.DataFrame(data)

    # Aseguramos que 'fecha' sea tipo datetime
    df['fecha'] = pd.to_datetime(df['fecha'])

    return df

# --- 3. Lógica de Filtros (Barra Lateral) ---

def create_sidebar(df):
    """
    Crea la barra lateral de control y aplica los filtros de Producto y Fecha.
    """
    with st.sidebar:
        st.header("Controles de Filtro")

        # Filtro de Producto (Multiselect)
        all_products = df['producto'].unique()
        producto_seleccionado = st.multiselect(
            "Filtrar Producto",
            options=all_products,
            default=all_products
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
        df_filtrado = df_filtrado[
            (df_filtrado['fecha'].dt.date >= start) &
            (df_filtrado['fecha'].dt.date <= end)
            ]

    st.sidebar.info(f"Registros filtrados: {len(df_filtrado):,}")

    return df_filtrado, date_range

# --- 4. Cálculo y Despliegue de Métricas (Delta Dinámico) ---

def calculate_delta(current_value, prior_value):
    """Calcula el porcentaje de cambio entre el valor actual y el valor anterior."""
    if prior_value == 0 or prior_value is None or prior_value == 0.0:
        return None
    return ((current_value - prior_value) / prior_value) * 100

def display_metrics(df_actual, df_original, date_range):
    """
    Calcula el periodo anterior, el delta y muestra las métricas en un contenedor.
    """

    # Contenedor visual para las métricas
    with st.container(border=True):
        st.subheader("Indicadores Clave (vs. Periodo Anterior)")

        df_prior = None

        # 4.1 Definición del Periodo Anterior
        if len(date_range) == 2:
            start_date, end_date = date_range
            period_duration = (end_date - start_date).days + 1
            prior_end_date = start_date - timedelta(days=1)
            prior_start_date = prior_end_date - timedelta(days=period_duration - 1)

            # Filtrar el DataFrame original para obtener el periodo anterior
            df_prior = df_original[
                (df_original['fecha'].dt.date >= prior_start_date) &
                (df_original['fecha'].dt.date <= prior_end_date)
                ]

            # Aplicar filtro de productos a df_prior
            productos_actuales = df_actual['producto'].unique()
            df_prior = df_prior[df_prior['producto'].isin(productos_actuales)]


        col1, col2, col3 = st.columns(3)

        # --- Métrica 1: Ventas Totales ---
        with col1:
            total_venta_actual = df_actual['ventas'].sum()
            total_venta_prior = df_prior['ventas'].sum() if df_prior is not None else 0

            delta_venta = calculate_delta(total_venta_actual, total_venta_prior)
            delta_str = f"{delta_venta:.2f}%" if delta_venta is not None else 'N/A'

            st.metric(
                "Ventas Totales",
                f"${total_venta_actual:,.0f}",
                delta=delta_str
            )

        # --- Métrica 2: Productos Activos (Únicos) ---
        with col2:
            productos_unicos_actual = df_actual['producto'].nunique()
            productos_unicos_prior = df_prior['producto'].nunique() if df_prior is not None else 0

            delta_productos = productos_unicos_actual - productos_unicos_prior

            st.metric(
                "Productos Activos",
                productos_unicos_actual,
                delta=delta_productos
            )

        # --- Métrica 3: Promedio de Venta ---
        with col3:
            promedio_venta_actual = df_actual['ventas'].mean()
            promedio_venta_prior = df_prior['ventas'].mean() if df_prior is not None and not df_prior.empty else 0

            delta_promedio = calculate_delta(promedio_venta_actual, promedio_venta_prior)

            # Formato de delta
            if delta_promedio is None:
                delta_str_promedio = 'N/A'
            else:
                delta_str_promedio = f"{delta_promedio:.2f}%"

            st.metric(
                "Venta Promedio",
                f"${promedio_venta_actual:,.0f}",
                delta=delta_str_promedio
            )


# --- 5. Despliegue de Gráficos, Tabla y Exportación ---

def display_charts(df):
    """
    Crea y muestra los tres gráficos, el botón de descarga y la tabla de datos.
    """
    st.subheader("Visualizaciones Detalladas")

    # 5.1 Fila superior de gráficos (Línea y Barras)
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown("##### Tendencia de Ventas Diarias (Línea)")
        # Agrupamos las ventas por día para la tendencia
        df_tendencia = df.groupby(df['fecha'].dt.date)['ventas'].sum().reset_index()
        df_tendencia.columns = ['Fecha', 'Ventas']

        fig_lineas = px.line(
            data_frame=df_tendencia,
            x='Fecha',
            y='Ventas',
            template='plotly_dark'
        )
        fig_lineas.update_layout(height=450, margin=dict(t=30, b=0, l=0, r=0))
        st.plotly_chart(fig_lineas, use_container_width=True)

    with col_chart2:
        st.markdown("##### Ventas Agrupadas por Artículo (Barras)")

        # Agrupar y sumar las ventas por producto
        ventas_por_producto = df.groupby('producto')['ventas'].sum().reset_index()
        ventas_por_producto.columns = ['Producto', 'Ventas']

        fig_barras = px.bar(
            data_frame=ventas_por_producto,
            x='Producto',
            y='Ventas',
            template='plotly_dark'
        )
        fig_barras.update_layout(height=450, margin=dict(t=30, b=0, l=0, r=0))
        st.plotly_chart(fig_barras, use_container_width=True)


    st.markdown("---")

    # 5.2 Fila inferior (Distribución y Descarga)
    col_pie_chart, col_download = st.columns([1, 1])

    with col_pie_chart:
        st.markdown("##### Distribución Porcentual de Ventas")
        ventas_por_producto = df.groupby('producto')['ventas'].sum().reset_index()
        ventas_por_producto.columns = ['Producto', 'Ventas']

        fig_pie = px.pie(
            ventas_por_producto,
            values='Ventas',
            names='Producto',
            hole=0.3, # Efecto de "dona"
            template='plotly_dark'
        )
        # Ocultamos la leyenda si hay demasiados productos para evitar desorden
        if len(ventas_por_producto) > 8:
            fig_pie.update_layout(showlegend=False)

        fig_pie.update_layout(height=350, margin=dict(t=30, b=0, l=0, r=0))
        st.plotly_chart(fig_pie, use_container_width=True)


    with col_download:
        # 5.3 Botón de Descarga
        st.markdown("##### Exportar Datos Filtrados")
        st.write("Utiliza este botón para descargar el conjunto de datos detallados, tal como aparecen tras aplicar los filtros.")

        # Función para convertir el DataFrame a CSV
        @st.cache_data
        def convert_df_to_csv(df):
            return df.to_csv(index=False).encode('utf-8')

        csv = convert_df_to_csv(df)

        st.download_button(
            label="Descargar Datos Filtrados (.csv)",
            data=csv,
            file_name=f'reporte_ventas_{datetime.now().strftime("%Y%m%d")}.csv',
            mime='text/csv',
            key='download_button'
        )

        st.markdown("---")


    # 5.4 Expander para la Tabla
    with st.expander("Ver datos detallados de la tabla y formato", expanded=False):
        st.markdown("##### Datos Brutos Filtrados")

        # Aplicar formato de moneda y fecha usando Pandas Styler para mejor visualización
        st.dataframe(
            df.style.format({
                'fecha': lambda t: t.strftime('%Y-%m-%d %H:%M'),
                'ventas': '${:,.2f}'
            }),
            use_container_width=True
        )


# --- 6. Función Principal del Dashboard ---

def main():
    """
    Orquesta el flujo completo de la aplicación Streamlit.
    """
    st.title("📊 Dashboard de Ventas Profesional con Streamlit")
    st.markdown("Esta aplicación demuestra la creación de un dashboard interactivo completo, simulando la carga de datos de una base de datos para análisis.")

    # 1. Cargar datos (simulados)
    df_original = load_data()

    # 2. Crear barra lateral y obtener datos filtrados y rango de fechas
    df_filtrado, date_range = create_sidebar(df_original)

    # 3. Mostrar las métricas con cálculo de delta dinámico
    display_metrics(df_filtrado, df_original, date_range)

    # 4. Mostrar gráficos, distribución, descarga y tabla
    display_charts(df_filtrado)

if __name__ == '__main__':
    main()
