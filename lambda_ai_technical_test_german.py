import hashlib
import boto3
import time
import json


## ai-technical-test-german
##Author: German Daniel Rojas 
## Funcion que procesa los archivos


def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    response = s3.get_object(Bucket=bucket, Key=key)  ## Obtiene el archivo  del bucket

    is_validate, map_file, status = process_file(response)  ##Extrae el contenido del archivo plano .txt

    if(status == False):
        print("Error al procesar el archivo")
        return{
            'statusCode': 500,
            'body': 'Error al procesar el archivo'
        }

    if is_validate:
        store_information_dynamo(map_file) ##Almacena la informacion en DynamoDB
        status_delete = delete_file(bucket, key) ##Elimina el archivo procesado del bucket
        if(status_delete == 1):
            return {
                'statusCode': 200,
                'body': "Proceso finalizado exitosamente"
            }
        else:
            return {
                'statusCode': 500,
                'body': "Error al eliminar el archivo"
            }
    else:
        print("El archivo no es valido")
        return{
            'statusCode': 400,
            'body': 'El archivo no es valido'
        }



##Extrae el contenido del archivo plano .txt
def process_file(response):
    status = False
    try:
        content = response['Body'].read().decode('utf-8')
        map_file = {}
        string_value_base = ""
        is_validate = False
        with open(content, 'r') as file:
            file_content = file.readline()
            for line in file_content:
                key, value = line.split('=')  ##Extrae el key y el value
                map_file[key] = value
                string_value_base += value + "~"
        string_value_base = string_value_base[:-1] ##Elimina el ultimo caracter "~" que sobra
        is_validate = validate_hash_md5(string_value_base, map_file['hash'])
        status = True
        return is_validate, map_file, status ##Retorna la validación hash, map_file y el status


    except Exception as e:
        print("Error al procesar el archivo:", e)
        return False, {}, status


##Comprueba y valida hash MD5
def validate_hash_md5(string_values_base, hash_md5_compare):
    hash_md5_base = hashlib.md5(string_values_base.encode('utf-8')).hexdigest()
    return hash_md5_base == hash_md5_compare


##Almacena la informacion en DynamoDB
def store_information_dynamo(map_file):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('ai-technical-test-german')
    map_file["timestamp"] = int(time.time())
    try:
        response = table.put_item(Item=map_file)
        print("Registro almacenado exitosamente:", response)
        return True
    except Exception as e:
        print("Error al almacenar el registro:", e)
        return {
            'statusCode': 500,
            'body': 'Error al almacenar el registro'
        }



##Elimina el archivo procesado del bucket
def delete_file(bucket, key):
    s3 = boto3.resource('s3')
    try:
        s3.Object(bucket, key).delete()
        print("Archivo eliminado exitosamente")
        return 1
    except Exception as e:
        print("Error al eliminar el archivo:", e)
    return 0


lambda_handler('', '')
