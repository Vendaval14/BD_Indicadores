# config.py - Variables globales de configuración

# Datos del servidor. 127.0.0.1 siempre apunta a tu propia computadora.
SQL_SERVER = "127.0.0.1"
DATABASE_MASTER = "master"  # Base de datos del sistema para operaciones de borrado/creación.
DATABASE_FINAL = "BD_Indicadores" # Tu base de datos de trabajo real.

# Estas son las credenciales que Python usará para "tocar la puerta" de SQL.
SQL_USER = "diresa"
SQL_PASS = "urico"

# Rutas de Windows. Usamos la 'r' (raw string) al inicio para que Python 
# no se confunda con las barras invertidas (\) de las carpetas.
RUTA_SQL_CREACION = r'C:\Indicadores2022\CONEXION\BD_Indicadores.sql'
RUTA_CARPETA_CSV  = r'C:\Indicadores2022\CSV'