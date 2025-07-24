# Wenia Product Operations Test

Este proyecto ha sido desarrollado por **Miguel Castellanos** como parte del proceso de selección para la posición de **Product Operations** en **Wenia**.

## Descripción

El repositorio contiene los entregables y documentación relacionados con la prueba técnica solicitada por el equipo de Wenia.



## Configuración

### Archivos
Rexuerda poner los archivos del input de la prueba en /output/s3Files, lo que pongas ahi se subira al bucket de s3 y seguira todo el flujo que se solicito

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

### ToDo
Por tiempo queda pendiente
* 5. Con las direcciones resultantes debes consumir el API de Google para obtener las coordenadas
exactas de la dirección y agregarlas a la tabla resultante donde están las direcciones que tenían
un porcentaje de similitud mayor al 90%.
* 6. Con estas coordenadas requerimos que presente un mapa donde se vean las diferentes
coordenadas resultantes.
* Pruebas Unitarias.
* SOPs y propuestas de mejora del proceso actual descrito en la prueba.
