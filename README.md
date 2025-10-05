📊 Dashboard de Ventas Profesional con Streamlit
Este proyecto es una aplicación de dashboard de ventas interactiva, desarrollada completamente en Python utilizando el framework Streamlit. Su objetivo es demostrar cómo crear visualizaciones de datos profesionales de forma rápida, sin necesidad de usar HTML, CSS o JavaScript, y simulando la conexión a una base de datos para cargar la información.

🌟 Características
Interfaz Profesional: Diseño moderno y responsivo gracias a Streamlit y Plotly.

Datos Simulados: No requiere una conexión externa a MySQL. Los datos de ventas son generados aleatoriamente con Pandas y NumPy.

Métricas Clave: Muestra el total de ventas, productos activos y promedio diario con indicadores de crecimiento.

Visualizaciones Interactivas: Incluye un gráfico de línea para la tendencia de ventas y un gráfico de barras para las ventas por producto.

Filtros de Datos: Permite filtrar los datos mostrados por Producto y por Rango de Fechas a través de una barra lateral.

Optimización de Carga: Utiliza el decorador @st.cache_data para simular la persistencia y velocidad de carga de datos, replicando la eficiencia de una conexión a una base de datos real.

# 🛠️ Configuración y Ejecución
Sigue estos pasos para poner en marcha el dashboard en tu entorno local.

Requisitos
Necesitas tener instalado Python 3.8+ en tu sistema.

1. Clonar el Repositorio (Opcional)
Si este es un repositorio, clónalo:

git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_DIRECTORIO>

2. Entorno Virtual
Es altamente recomendado usar un entorno virtual para aislar las dependencias del proyecto.

# Crear el entorno virtual (venv es un nombre común)
python -m venv venv

# Activar el entorno virtual
# En Windows (CMD):
# venv\Scripts\activate
# En Linux/macOS o PowerShell:
source venv/bin/activate

3. Instalación de Dependencias
Instala todas las librerías necesarias (Streamlit, Pandas, Plotly y NumPy).

pip install streamlit pandas plotly numpy

4. Ejecución de la Aplicación
Una vez que tengas el archivo app.py y las librerías instaladas, ejecuta el dashboard usando el comando de Streamlit:

streamlit run app.py

Streamlit iniciará el servidor web y automáticamente abrirá la aplicación en tu navegador predeterminado (generalmente en http://localhost:8501).

⚙️ Estructura del Código
El archivo app.py está estructurado en funciones para mejorar la modularidad y la legibilidad:

Función

Descripción

load_data()

Genera los datos simulados de ventas y los cachea usando @st.cache_data.

create_sidebar(df)

Crea los filtros interactivos en la barra lateral y retorna el DataFrame filtrado.

display_metrics(df)

Calcula y muestra las tres métricas principales con sus indicadores delta.

display_charts(df)

Genera y presenta los gráficos de línea y barras, además del expander con los datos detallados.

main()

La función principal que orquesta la carga de datos, los filtros y el despliegue de la interfaz.

💡 Cómo Adaptarlo a una Base de Datos Real
Si en el futuro deseas conectar esto a una base de datos real (como MySQL o PostgreSQL), solo necesitas modificar la función load_data():

Reemplaza la lógica de generación de datos de Pandas por la lógica de conexión y consulta a tu base de datos.

Asegúrate de importar la librería de conexión adecuada (ej: mysql.connector).

Mantén el decorador @st.cache_data para asegurar que los datos solo se consulten una vez, mejorando drásticamente el rendimiento de la aplicación.
