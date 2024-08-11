import boto3
import os
import uuid

def new_post_handler(event, context) -> str:
    recordId = str(uuid.uuid4())
    voice = event['voice']
    text = event['text']

    print('Generating new DynamoDB record, with ID: ' + recordId)
    print('Input Text: ' + text)
    print('Selected voice: ' + voice)

    # Create new record in DynamoDB table
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DB_TABLE_NAME'])
    table.put_item(
        Item={
            'id': recordId,
            'text': text,
            'voice': voice,
            'status': 'PROCESSING'
        }
    )

    # Sending notification to SNS topic
    sns_client = boto3.client('sns')
    sns_client.publish(
        TopicArn=os.environ['SNS_TOPIC_ARN'],
        Message=recordId
    )

    return recordId