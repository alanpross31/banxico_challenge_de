# Introducción
Este es un repositorio para la solución del challenge de Data Engineer para Quantum. El challenge era crear un API para poder traer el tipo de cambio del dollar de una rango de fecha específica de la API SIE de Banxico.

## Arquitectura
La arquitectura que elegí para la solución del challenge es el siguente:
![quantum_challenge drawio](https://github.com/user-attachments/assets/72b348a6-40a8-400e-83df-3b90b03dab42)

AWS Lambda: Maneja la extracción de datos de la API de Banxico, procesa los datos y los almacena en S3.
Amazon S3: Almacena los datos JSON extraídos por la función Lambda en una capa raw.
AWS Glue: Lo utilizaremos para poder transformar  el json en un dataframe con pandas y poder crear una tabla en Redshift con el histórico de la inforación.
Amazon Redshift: Crearemos la tabla con la información del tipo de cambio.
Amazon CloudWatch: Nos permitira monitorear la función lambda y alertas en los logs.

## lambda
Contiene el script para poder extraer la información por medio le lambda, donde tomara 3 parametros para pode ejecutar (serie,fecha_inicio,fecha_fin), y alojará el resultado en bucket "raw"

## terraform
Aquí estará los archivos tf que nos ayudarán a desplegar los servicio en AWS. Aquí no hice el despliegue como tal de todos los servicio, ya que ocupé mi cuenta personal y evite el cargo extra de algunos servicios, sin embargo pusé el código que hubiera utilizado para el despliegue.

## etl
Añadí un código en python para poder ejecutar con glue, este script permité crear un dataframe a partir del json que nos arrojó nuestro llamado API.
