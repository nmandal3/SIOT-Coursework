import boto3

def lambda_handler(event, context):
    client = boto3.client('dynamodb')
    
    response = client.put_item(
        TableName = 'nainipidataV3',
        Item = {
            'timestamp': {'S': event['timestamp']},
            'gsr': {'N': str(event['gsr'])},
            'stemp': {'N': str(event['stemp'])},
            'shumidity': {'N': str(event['shumidity'])},
            'apitemperature': {'N': str(event['apitemperature'])},
            'apihumidity': {'N': str(event['apihumidity'])},
            'so2': {'N': str(event['so2'])},
            'no2': {'N': str(event['no2'])},
            'pm10': {'N': str(event['pm10'])},
            'pm25': {'N': str(event['pm25'])}
        }
    )
    
    return 0
    