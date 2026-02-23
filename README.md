# Sistema de Gestión de Indicadores de Salud - BD_Indicadores

Este proyecto contiene la lógica de base de datos y scripts de procesamiento para el análisis de indicadores sanitarios, desarrollado sobre **SQL Server 2014**.

## 🚀 Configuración del Entorno

Para que los scripts de carga funcionen correctamente, es obligatorio seguir esta estructura:

### 1. Datos (Archivos CSV)
Los archivos de la trama nominal y maestros deben estar ubicados en la siguiente ruta absoluta:
`C:\Indicadores2022\CSV\`

La estructura de carpetas dentro de CSV debe incluir:
- `\maestros\` (Pacientes, Personal, Registrador, Padrón)
- `\2021\` hasta `\2026\` (Archivos mensuales en formato .csv)

### 2. Base de Datos
1. Ejecutar el script de creación de tablas en la base de datos `BD_Indicadores`.
2. Asegurarse de tener creadas las funciones de cálculo de edad:
   - `Edad_Meses`
   - `fn_Calcula_Edad`
   - `fn_Calcula_EdadMeses`

## 🛠️ Flujo de Trabajo (Git)

- **Rama `master`**: Versión estable del proyecto. No realizar cambios directos aquí.
- **Rama `desarrollo-indicadores-2`**: Rama de trabajo para nuevas implementaciones y correcciones.

### Comandos útiles para el colaborador:
```bash
# Cambiar a la rama de trabajo
git checkout desarrollo-indicadores-2

# Subir avances
git add .
git commit -m "Descripción del cambio"
git push origin desarrollo-indicadores-2