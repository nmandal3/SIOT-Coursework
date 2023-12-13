import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('nainipidataV3')

    response = table.scan()
    
    items = response['Items']
    items.sort(key=lambda x: x['timestamp'], reverse=True)
    
    lastItem = items[0]
    gsr_value = lastItem['gsr']
    time_value = lastItem['timestamp']
    
    #Threshold value for 'gsr'
    gsr_threshold = 550

    if gsr_value > gsr_threshold:
        # Send SMS using SNS
        sns_client = boto3.client('sns')
        topic_arn = 'omitted for privacy:SMSsend'
        
        msg = "Your skin is beginning to look quite dry, why not moisturise?"
        sns_client.publish(TopicArn=topic_arn, Message=msg)
        
        oldMessage = f"Threshold exceeded for 'gsr' {gsr_value} in the latest item: {time_value}"

    return items
