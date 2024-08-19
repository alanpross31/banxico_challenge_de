import json
import requests
import boto3
from datetime import datetime

def lambda_handler(event, context):
    # Calcula la fecha de termino a paritr de la feche de ejeucccion 
    end_date = datetime.now().strftime("%Y-%m-%d")
    
    # Calcula la fecha de inicio del mes tomando como parametro la fecha de ejecución de la función
    start_date = datetime.now().replace(day=1).strftime("%Y-%m-%d")
    
    # API endpoint par
    base_url = "https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF63528"
    series_id = event.get("series_id", "SF63528")
    token = "5a9a46c57fa389aa6f9e3044ed6222169f8f87ceedc621524fe32ad1fee109e2" 
    
    # S3 b
    s3_bucket_name = "banxico-tipo-de-cambio-dollar-raw"
    s3_key = f"banxico_data/{series_id}_{start_date}_to_{end_date}.json"

    # URL para la peticion de infromación
    url = f"{base_url}/{series_id}/{start_date}/{end_date}"

    # Setting headers for the API request
    headers = {
        "Bmx-Token": token
    }

    # Making the GET request to the API
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parsing the JSON response
        data = response.json()

        # Extracting relevant data
        series_data = data.get('bmx', {}).get('series', [])

        # Convert series_data to a JSON string
        json_data = json.dumps(series_data)

        # Initialize S3 client
        s3 = boto3.client('s3')

        # Upload the JSON data to S3
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
        # Handle errors from the API request
        return {
            'statusCode': response.status_code,
            'body': json.dumps({
                'error': 'Failed to retrieve data',
                'message': response.text
            })
        }
