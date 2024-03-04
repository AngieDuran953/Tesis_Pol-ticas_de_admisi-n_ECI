# Asistente de Limpieza de Datos

## Descripción
Esta aplicación web, desarrollada en Flask, permite a los usuarios cargar archivos CSV para su análisis y limpieza. Admite varios tipos de archivos con columnas requeridas específicas y realiza una limpieza de datos básica, como eliminar espacios extras, caracteres especiales y convertir tipos de datos adecuadamente.

## Características
- Carga de archivos CSV.
- Verificación de columnas requeridas basadas en el tipo de archivo.
- Limpieza de datos incluyendo normalización de texto y conversión de tipos de datos.
- Descarga de archivos CSV procesados.

## Tecnologías Utilizadas
- Python
- Flask
- Pandas
- HTML/CSS

## Instalación y Ejecución

### Requisitos Previos
Asegúrate de tener Python 3.6 o superior instalado en tu sistema.

### Pasos
1. Clona este repositorio a tu máquina local.
2. Navega al directorio del proyecto clonado.
3. Crea un entorno virtual:


4. Activa el entorno virtual:
- En Windows:

  ```
  venv\Scripts\activate
  ```

- En macOS y Linux:

  ```
  source venv/bin/activate
  ```

5. Instala las dependencias del proyecto:


6. Ejecuta la aplicación


7. Abre un navegador y navega a `http://127.0.0.1:5000/` para acceder a la aplicación.

## Uso
- En la página principal, selecciona el tipo de archivo que deseas cargar.
- Haz clic en "Cargar y Limpiar" para subir tu archivo CSV.
- Si el archivo cumple con los requisitos, será procesado y recibirás un enlace para descargar el archivo limpio.

## Contribuciones
Las contribuciones son bienvenidas. Si tienes ideas para mejorar la aplicación o añadir nuevas características, no dudes en crear un pull request.

## Licencia
Este proyecto está bajo [INSERTE EL TIPO DE LICENCIA AQUÍ] - vea el archivo LICENSE.md para más detalles.

