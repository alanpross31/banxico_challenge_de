import boto3
import json
import pandas as pd
from io import BytesIO

def read_json_from_s3(bucket_name, key):
    """
    Read a JSON file from S3 and return it as a dictionary.
    """
    s3 = boto3.client('s3')
    
    response = s3.get_object(Bucket=bucket_name, Key=key)
    content = response['Body'].read()
    
    # Convertimos el json en un diccionario
    data = json.loads(content)
    
    return data

def transform_to_dataframe(json_data):
    """
    Transform the JSON data into a pandas DataFrame.
    """
    records = []
    for serie in json_data['bmx']['series']:
        for dato in serie['datos']:
            records.append({
                'idSerie': serie['idSerie'],
                'titulo': serie['titulo'],
                'fecha': dato['fecha'],
                'dato': float(dato['dato'])
            })
    
    # Convetimo la lista en un dataframe
    df = pd.DataFrame(records)
    
    return df

def main():
    
    bucket_name = 'banxico-tipo-de-cambio-dollar-raw'
    key = 'banxico_data/SF63528_2024-02-01_to_2024-02-29.json'
    
    # Va por el nombre del bucket para leer los datos
    json_data = read_json_from_s3(bucket_name, key)

    df = transform_to_dataframe(json_data)
    print(df)

if __name__ == "__main__":
    main()