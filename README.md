## ai-technical-test-german
# Función Lambda de Procesamiento de Archivos

Esta función Lambda procesa archivos de texto plano (.txt) almacenados en Amazon S3. Una vez que se detecta un nuevo archivo en el bucket de S3 especificado, esta función realiza varias operaciones, incluyendo la validación del archivo, el almacenamiento de la información en DynamoDB y la eliminación del archivo procesado del bucket.

## Autor
- **Autor:** German Daniel Rojas

## Requisitos
- Python 3.10
- AWS SDK for Python (Boto3)
- Acceso a Amazon S3 y Amazon DynamoDB

## Uso
La función Lambda es desencadenada por eventos de S3 cuando se carga un nuevo archivo en el bucket especificado. Para configurar el desencadenador de eventos de S3, asegúrate de que la función Lambda tenga permisos adecuados para acceder al bucket de S3 y sus objetos.

## Funcionamiento
1. Cuando se detecta un nuevo archivo en el bucket de S3, la función Lambda obtiene el contenido del archivo y lo procesa.
2. El contenido del archivo se divide en líneas y se mapea en un diccionario de clave-valor.
3. Se valida el hash MD5 del contenido del archivo para garantizar su integridad.
4. La información del archivo se almacena en una tabla de DynamoDB junto con un timestamp para realizar un seguimiento de cuándo se procesó el archivo.
5. Una vez que la información se almacena correctamente en DynamoDB, el archivo procesado se elimina del bucket de S3.

## Código
El código de la función Lambda está escrito en Python y se encuentra en el archivo `app.py`.

## Configuración
- Asegúrate de que la función Lambda tenga permisos adecuados para acceder a los servicios de AWS, incluyendo S3 y DynamoDB.
- Configura el desencadenador de eventos de S3 para que la función Lambda sea activada cuando se cargue un nuevo archivo en el bucket especificado.
