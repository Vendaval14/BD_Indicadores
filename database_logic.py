# ============================================================
# MÓDULO: database_logic.py
# DESCRIPCIÓN: Contiene toda la lógica de conexión y operaciones
#              sobre la base de datos SQL Server del proyecto.
# ============================================================

import pyodbc   # Librería para conectarse a bases de datos mediante ODBC (Open Database Connectivity)
import config   # Módulo propio del proyecto que contiene las variables de configuración (servidor, usuario, contraseña, rutas, etc.)
import os       # Módulo estándar de Python para interactuar con el sistema operativo (rutas, carpetas, archivos)
import re       # Módulo estándar de Python para trabajar con expresiones regulares (búsqueda y división de texto)


# ─────────────────────────────────────────────────────────────
# FUNCIÓN: obtener_string_conexion
# PROPÓSITO: Construir y retornar la cadena de conexión ODBC
#            para conectarse a una base de datos específica.
# ─────────────────────────────────────────────────────────────
def obtener_string_conexion(db_name):
    """Genera la cadena de conexión con credenciales de SQL Server."""

    return (                                    # Retorna la cadena de conexión armada con f-strings
        f"DRIVER={{SQL Server}};"               # Especifica el driver ODBC a usar: "SQL Server" (las llaves dobles {{ }} son para escapar las llaves literales en f-strings)
        f"SERVER={config.SQL_SERVER};"          # Nombre o IP del servidor SQL Server, leído desde config.py
        f"DATABASE={db_name};"                  # Nombre de la base de datos a la que se conectará (recibido como parámetro)
        f"UID={config.SQL_USER};"               # Usuario de SQL Server, leído desde config.py
        f"PWD={config.SQL_PASS};"               # Contraseña del usuario SQL Server, leída desde config.py
    )


# ─────────────────────────────────────────────────────────────
# FUNCIÓN: ejecutar_reconstruccion
# PROPÓSITO: Conectarse a la base de datos maestra y ejecutar
#            el script SQL que crea (o recrea) la base de datos
#            y sus tablas desde cero.
# ─────────────────────────────────────────────────────────────
def ejecutar_reconstruccion():
    """Ejecuta el script de creación de base de datos y tablas."""

    try:                                                                        # Inicia bloque de manejo de errores
        conn_str = obtener_string_conexion(config.DATABASE_MASTER)              # Obtiene la cadena de conexión apuntando a la base de datos maestra (master), necesaria para crear otras bases de datos
        conn = pyodbc.connect(conn_str, autocommit=True)                        # Abre la conexión con SQL Server; autocommit=True ejecuta cada sentencia inmediatamente sin necesidad de hacer COMMIT manual
        cursor = conn.cursor()                                                  # Crea un cursor, que es el objeto que permite enviar y ejecutar sentencias SQL

        with open(config.RUTA_SQL_CREACION, 'r', encoding='latin-1') as f:     # Abre el archivo .sql de creación en modo lectura ('r'), usando codificación latin-1 (común en scripts SQL de SQL Server en español)
            script = f.read()                                                   # Lee todo el contenido del archivo SQL y lo guarda como una cadena de texto en la variable 'script'

        bloques = re.split(r'\bGO\b', script, flags=re.IGNORECASE)             # Divide el script en bloques separados por la palabra "GO" (separador de lotes en T-SQL); \b asegura que sea una palabra completa; re.IGNORECASE ignora mayúsculas/minúsculas
        for bloque in bloques:                                                  # Itera sobre cada bloque de sentencias SQL resultante de la división
            if bloque.strip():                                                  # Verifica que el bloque no esté vacío (strip() elimina espacios y saltos de línea al inicio y al final)
                cursor.execute(bloque.strip())                                  # Ejecuta el bloque SQL en la base de datos, eliminando espacios innecesarios

        conn.close()                                                            # Cierra la conexión con la base de datos para liberar recursos
        return True, "Base de Datos y Tablas Recreadas con éxito"               # Retorna una tupla indicando éxito (True) y un mensaje descriptivo

    except Exception as e:                                                      # Captura cualquier error que ocurra durante el proceso
        return False, f"Error en Reconstrucción: {str(e)}"                     # Retorna una tupla indicando fallo (False) y el mensaje de error convertido a texto


# ─────────────────────────────────────────────────────────────
# FUNCIÓN: ejecutar_carga_datos  (OPCIÓN A)
# PROPÓSITO: Ejecutar un script SQL fijo (CargaMasiva.sql) que
#            limpia las tablas y carga los datos maestros y
#            tramas predefinidas en la base de datos final.
# ─────────────────────────────────────────────────────────────
def ejecutar_carga_datos():
    """
    OPCIÓN A: Ejecuta CargaMasiva.sql.
    Ideal para limpiar tablas y cargar maestros/tramas fijas según tu script.
    """

    conn_str = obtener_string_conexion(config.DATABASE_FINAL)                   # Obtiene la cadena de conexión apuntando a la base de datos final (donde viven los datos del proyecto)

    try:                                                                        # Inicia bloque de manejo de errores
        conn = pyodbc.connect(conn_str, autocommit=True)                        # Abre la conexión con SQL Server con autocommit activado
        cursor = conn.cursor()                                                  # Crea el cursor para ejecutar sentencias SQL

        # Ruta definida según tu requerimiento
        ruta_carga = r'C:\Indicadores2022\CONEXION\CargaMasiva.sql'             # Define la ruta absoluta del archivo SQL de carga masiva (la 'r' antes de la cadena indica raw string, evitando que las barras invertidas se interpreten como caracteres especiales)

        # 'utf-8-sig' detecta y elimina automáticamente esos caracteres invisibles (BOM)
        with open(ruta_carga, 'r', encoding='utf-8-sig') as f:                  # Abre el archivo CargaMasiva.sql en modo lectura con codificación latin-1
            script = f.read()                                                   # Lee todo el contenido del archivo SQL como texto

        bloques = re.split(r'\bGO\b', script, flags=re.IGNORECASE)             # Divide el script en bloques usando "GO" como separador de lotes T-SQL, ignorando mayúsculas/minúsculas
        for bloque in bloques:                                                  # Itera sobre cada bloque SQL resultante
            comando = bloque.strip()                                            # Elimina espacios y saltos de línea al inicio y al final del bloque y lo guarda en 'comando'
            if comando:                                                         # Verifica que el bloque no esté vacío antes de ejecutarlo
                cursor.execute(comando)                                         # Ejecuta el bloque SQL en la base de datos

        conn.close()                                                            # Cierra la conexión con la base de datos
        return True, "Maestros y Tramas actualizados (Script SQL) correctamente."  # Retorna éxito (True) con mensaje descriptivo

    except Exception as e:                                                      # Captura cualquier excepción que ocurra
        return False, f"Error en Carga Masiva SQL: {str(e)}"                   # Retorna fallo (False) con el mensaje de error


# ─────────────────────────────────────────────────────────────
# FUNCIÓN: ejecutar_carga_masiva_dinamica  (OPCIÓN B)
# PROPÓSITO: Recorrer automáticamente carpetas organizadas por
#            año, buscar archivos CSV y cargarlos en la tabla
#            NOMINAL_TRAMA usando BULK INSERT dinámico.
# ─────────────────────────────────────────────────────────────
def ejecutar_carga_masiva_dinamica():
    """
    OPCIÓN B: Carga dinámica por carpetas.
    Busca automáticamente archivos CSV por año sin necesidad de editar el .sql.
    """

    try:                                                                        # Inicia bloque de manejo de errores
        conn_str = obtener_string_conexion(config.DATABASE_FINAL)               # Obtiene la cadena de conexión a la base de datos final
        conn = pyodbc.connect(conn_str, autocommit=True)                        # Abre la conexión con SQL Server con autocommit activado
        cursor = conn.cursor()                                                  # Crea el cursor para ejecutar sentencias SQL

        anios = ['2021', '2022', '2023', '2024', '2025', '2026']               # Define la lista de años a procesar; se buscará una subcarpeta por cada año
        archivos_procesados = 0                                                 # Inicializa el contador de archivos CSV procesados en cero

        for anio in anios:                                                      # Itera sobre cada año de la lista
            ruta_anio = os.path.join(config.RUTA_CARPETA_CSV, anio)            # Construye la ruta completa de la carpeta del año actual (ej: C:\CSV\2022)
            if os.path.exists(ruta_anio):                                       # Verifica si la carpeta del año existe en el sistema de archivos antes de intentar acceder a ella
                for archivo in os.listdir(ruta_anio):                          # Lista todos los archivos dentro de la carpeta del año e itera sobre ellos
                    if archivo.endswith('.csv'):                                # Filtra solo los archivos que tengan extensión .csv
                        ruta_completa = os.path.join(ruta_anio, archivo)       # Construye la ruta completa del archivo CSV (carpeta + nombre de archivo)

                        # BULK INSERT dinámico generado por Python
                        sql_bulk = f"""
                        BULK INSERT NOMINAL_TRAMA                               
                        FROM '{ruta_completa}'                                  
                        WITH (FIRSTROW = 2, FIELDTERMINATOR = ',', ROWTERMINATOR='\\n');
                        """
                        # ↑ Genera dinámicamente la sentencia T-SQL BULK INSERT:
                        #   - NOMINAL_TRAMA: tabla destino donde se insertarán los datos
                        #   - FROM: ruta del archivo CSV a cargar
                        #   - FIRSTROW = 2: omite la primera fila (encabezados del CSV)
                        #   - FIELDTERMINATOR = ',': indica que los campos están separados por coma
                        #   - ROWTERMINATOR = '\n': indica que cada fila termina con salto de línea

                        cursor.execute(sql_bulk)                                # Ejecuta la sentencia BULK INSERT en SQL Server para cargar el archivo CSV en la tabla
                        archivos_procesados += 1                                # Incrementa el contador de archivos procesados en 1

        conn.close()                                                            # Cierra la conexión con la base de datos al finalizar todos los años
        return True, f"Carga Dinámica completada. {archivos_procesados} archivos procesados."   # Retorna éxito (True) con el total de archivos cargados

    except Exception as e:                                                      # Captura cualquier excepción que ocurra durante el proceso
        return False, f"Error en Carga Dinámica: {str(e)}"                     # Retorna fallo (False) con el mensaje de error detallado


def probar_conexion():
    """Verifica si Python puede entrar al SQL Server."""
    try:
        # Intentamos conectar a la base master para validar el acceso
        conn_str = obtener_string_conexion(config.DATABASE_MASTER)
        conn = pyodbc.connect(conn_str)
        conn.close()
        return True, "¡Conexión Exitosa con SQL Server!"
    except Exception as e:
        return False, f"Error de conexión: {str(e)}"