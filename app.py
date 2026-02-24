# Importa la librería Streamlit, que permite construir interfaces web interactivas con Python
import streamlit as st

# Importa el módulo database_logic (archivo database_logic.py) con alias 'db',
# que contiene todas las funciones de conexión y operaciones con la base de datos
import database_logic as db

# Importa el módulo config (archivo config.py) que contiene las variables de configuración
# como el servidor SQL, nombre de la base de datos, rutas, etc.
import config

# --- CONFIGURACIÓN ESTILO BOOTSTRAP ---

# Configura la página de Streamlit: define el título que aparece en la pestaña del navegador
# y establece el layout en "wide" para que el contenido ocupe todo el ancho de la pantalla
st.set_page_config(page_title="Gestión de Atenciones de Salud", layout="wide")

# Inyecta CSS personalizado dentro de la app usando HTML sin restricciones (unsafe_allow_html=True)
st.markdown("""
    <style>
    /* Hace que todos los botones de Streamlit ocupen el 100% del ancho del contenedor,
       tengan bordes redondeados, una altura fija y texto en negrita */
    .stButton>button { width: 100%; border-radius: 5px; height: 3.5em; font-weight: bold; }

    /* Clase CSS para botones de verificación: color de fondo celeste (Bootstrap info) */
    .btn-verif { background-color: #0dcaf0; }

    /* Clase CSS para botones de infraestructura: color de fondo gris (Bootstrap secondary) */
    .btn-infra { background-color: #6c757d; }

    /* Clase CSS para botones de maestros: color de fondo amarillo (Bootstrap warning) con texto negro */
    .btn-maestros { background-color: #ffc107; color: black; }

    /* Clase CSS para botones de tramas: color de fondo verde (Bootstrap success) con texto blanco */
    .btn-tramas { background-color: #198754; color: white; }
    </style>
    """, unsafe_allow_html=True)

# Muestra el título principal de la aplicación con un emoji de hospital
st.title("🏥 Aplicativo de Gestión: Indicadores FED 2026")

# Muestra un texto informativo con el servidor SQL y la base de datos a los que está conectado,
# tomando los valores directamente desde el módulo config
st.write(f"Conectado a: **{config.SQL_SERVER}** | Base de Datos: **{config.DATABASE_FINAL}**")

# Dibuja una línea divisoria horizontal para separar el encabezado del contenido principal
st.divider()

# --- COLUMNAS DE OPERACIÓN ---

# Divide la pantalla en 3 columnas de igual tamaño para organizar las secciones de la app
col1, col2, col3 = st.columns(3)

# ── COLUMNA 1: INFRAESTRUCTURA ──────────────────────────────────────────────
with col1:
    # Muestra un cuadro de información azul con el título de la sección
    st.info("### 1. Infraestructura")

    # Crea un botón "Probar Conexión"; si el usuario lo presiona, ejecuta el bloque interior
    if st.button("🔌 Probar Conexión"):
        # Llama a la función probar_conexion() del módulo db,
        # que devuelve una tupla (éxito: bool, mensaje: str)
        exito, msj = db.probar_conexion()

        # Si la conexión fue exitosa, muestra el mensaje en verde (success)
        if exito: st.success(msj)

        # Si falló, muestra el mensaje en rojo (error)
        else: st.error(msj)

    # Crea un botón "Recrear Base y Tablas"; si el usuario lo presiona, ejecuta el bloque interior
    if st.button("🏗️ Recrear Base y Tablas"):

        # Muestra un spinner (animación de carga) con un mensaje mientras se ejecuta la operación
        with st.spinner("Borrando y creando estructura..."):

            # Llama a la función ejecutar_reconstruccion() que borra y recrea la base de datos y sus tablas
            exito, msj = db.ejecutar_reconstruccion()

            # Si la reconstrucción fue exitosa, muestra el mensaje en verde
            if exito: st.success(msj)

            # Si falló, muestra el mensaje en rojo
            else: st.error(msj)

# ── COLUMNA 2: MAESTROS (SQL) ────────────────────────────────────────────────
with col2:
    # Muestra un cuadro de advertencia amarillo con el título de la sección
    st.warning("### 2. Maestros (SQL)")

    # Muestra un texto descriptivo explicando qué datos se cargan en esta sección
    st.write("Carga de Pacientes, Personal y Padrón Nominal mediante script.")

    # Crea un botón "Ejecutar Carga de Maestros"; si el usuario lo presiona, ejecuta el bloque interior
    if st.button("📊 Ejecutar Carga de Maestros"):

        # Muestra un spinner mientras se ejecuta la carga del archivo SQL
        with st.spinner("Cargando maestros desde CargaMasiva.sql..."):

            # Usamos la Opción A: Función que ejecuta tu .sql
            # Llama a la función ejecutar_carga_datos() que lee y ejecuta el script SQL de carga masiva
            exito, msj = db.ejecutar_carga_datos()

            # Si la carga fue exitosa, muestra el mensaje en verde
            if exito: st.success(msj)

            # Si falló, muestra el mensaje en rojo
            else: st.error(msj)

# ── COLUMNA 3: TRAMAS (PYTHON) ───────────────────────────────────────────────
with col3:
    # Muestra un cuadro de éxito verde con el título de la sección
    st.success("### 3. Tramas (Python)")

    # Muestra un texto descriptivo explicando el rango de años que se procesarán
    st.write("Carga automática de archivos CSV por años (2021-2025).")

    # Crea un botón "INICIAR CARGA DINÁMICA"; si el usuario lo presiona, ejecuta el bloque interior
    if st.button("🚀 INICIAR CARGA DINÁMICA"):

        # Muestra un spinner con un aviso de que el proceso puede demorar varios minutos
        with st.spinner("Procesando carpetas anuales... Esto puede tardar."):

            # Usamos la Opción B: Función que recorre carpetas
            # Llama a la función ejecutar_carga_masiva_dinamica() que recorre las carpetas
            # de cada año (2021-2025), lee los archivos CSV y los inserta en la base de datos
            exito, msj = db.ejecutar_carga_masiva_dinamica()

            # Si la carga fue exitosa, muestra el mensaje en verde
            if exito:
                st.success(msj)

                # Lanza una animación de globos de celebración en la pantalla
                st.balloons()

            # Si falló, muestra el mensaje en rojo
            else:
                st.error(msj)

# Dibuja otra línea divisoria horizontal para separar las columnas del reporte inferior
st.divider()

# --- REPORTE DE ESTADO ---

# Muestra un subtítulo para la sección de reporte
st.subheader("Estado de las Atenciones")

# Muestra un texto pequeño (caption) como nota informativa para el usuario
st.caption("Una vez finalizada la carga, podrás visualizar aquí el resumen de registros por año.")

# Dentro de app.py, puedes poner esto al principio de la barra lateral o del menú principal
st.sidebar.title("⚙️ Configuración Inicial")
if st.sidebar.button("🚀 Inicializar Sistema en esta PC"):
    con_exito, con_msj = db.configurar_entorno_inicial()
    if con_exito:
        st.sidebar.success(con_msj)
    else:
        st.sidebar.error(con_msj)