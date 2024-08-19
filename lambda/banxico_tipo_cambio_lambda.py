import json
import requests 
import boto3
from datetime import datetime

def lambda_handler(event, context):
    #Extrae la fecha de inicio y fecha fin

    start_date = event.get("start_date", None)
    end_date = event.get("end_date", None)

    #Si no se proporciona 2 fechas tomara la fecha de ejecucción por default
    if not start_date:
        start_date = datetime.now().replace(day=1).strftime("%Y-%m-%d")
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")
        
    # API endpoint par
    base_url = "https://www.banxico.org.mx/SieAPIRest/service/v1/series"
    series_id = event.get("series_id", "SF63528")
    token = "5a9a46c57fa389aa6f9e3044ed6222169f8f87ceedc621524fe32ad1fee109e2" 
    
    # S3 bucket
    s3_bucket_name = "banxico-tipo-de-cambio-dollar-raw"
    s3_key = f"banxico_data/{series_id}_{start_date}_to_{end_date}.json"

    # URL para la peticion de infromación
    url = f"{base_url}/{series_id}/datos/{start_date}/{end_date}?token={token}"

    # Declaramos el header
    headers = {
        "Bmx-Token": token
    }

    # Hacemos el request de la información 
    response = requests.get(url, headers=headers)

    # Verifica que el status sea 200 para poder continuar con al extracción
    if response.status_code == 200:
        
        data = response.json()

        # Extraemos los datos que necesitamos
        series_data = data.get('bmx', {}).get('series', [])

        # Convierte la respuesta en un json
        json_data = json.dumps(series_data)

       
        s3 = boto3.client('s3')

        # Subimos la información a nuestro bucket que definimos
        try:
            s3.put_object(
                Bucket=s3_bucket_name,
                Key=s3_key,
                Body=json_data,
                ContentType='application/json'
            )
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Data successfully uploaded to S3',
                    's3_bucket': s3_bucket_name,
                    's3_key': s3_key
                })
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'error': 'Failed to upload data to S3',
                    'message': str(e)
                })
            }

    else:
        # Si obtenemos un error los dara el codigo del error
        return {
            'statusCode': response.status_code,
            'body': json.dumps({
                'error': 'Failed to retrieve data',
                'message': response.text
            })
        }
