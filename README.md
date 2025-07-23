# Wenia Product Operations Test

Este proyecto ha sido desarrollado por **Miguel Castellanos** como parte del proceso de selección para la posición de **Product Operations** en **Wenia**.

## Descripción

El repositorio contiene los entregables y documentación relacionados con la prueba técnica solicitada por el equipo de Wenia.

## Autor

- Miguel Castellanos

## setup

### Configuración

/productTest
├── app/
│ └── s3upload.py ← aquí está el script
├── weniafiles/ ← aquí los archivos a subir a S3
├── .env

Duplica .env.example y renómbralo a .env con tus credenciales y ajustes:

AWS_ACCESS_KEY_ID=TU_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=TU_SECRET_ACCESS_KEY
AWS_REGION=us-east-1 # Ajusta tu región
S3_BUCKET=nombre-de-tu-bucket
LOCAL_DIR=weniafiles # Carpeta local a escanear
STATE_FILE=state.json # Archivo para registrar hashes

Guarda el archivo .env en la raíz del proyecto.

### Uso con Docker

Construir la imagen

docker build -t s3uploader .

Ejecutar el contenedor

docker run --rm \
 --env-file .env \
 -v $(pwd)/weniafiles:/app/weniafiles \
 s3uploader

Monta la carpeta local weniafiles en /app/weniafiles dentro del contenedor.

Lee variables de entorno desde tu .env.

El contenedor se elimina al terminar (--rm).
