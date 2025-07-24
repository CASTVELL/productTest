# Wenia Product Operations Test

Este proyecto ha sido desarrollado por **Miguel Castellanos** como parte del proceso de selección para la posición de **Product Operations** en **Wenia**.

## Descripción

El repositorio contiene los entregables y documentación relacionados con la prueba técnica solicitada por el equipo de Wenia.



## Configuración

### Copia el ejemplo de variables de entorno y edítalo:
.env.example

### aws 

En .env debes poner tus AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY y S3_BUCKET

Debes configurar las politicas del s3 buckets de acuerdos a los requerimientos de la prueba

### Construye y levanta el contenedor Docker:
docker-compose up --build -d

Verifica que el servicio esté corriendo:
docker ps

Inspecciona los logs:
docker logs -f s3sync

Para detener y eliminar el contenedor:
docker-compose down
