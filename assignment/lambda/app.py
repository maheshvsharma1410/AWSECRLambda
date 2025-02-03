import os
import json
import logging
import boto3
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME')
table = dynamodb.Table(table_name)

def validate_message(event):
    if "messageUUID" not in event or "messageText" not in event or "messageDatetime" not in event:
        return False, "Missing required fields"
    
    message_text = event["messageText"]
    if not isinstance(message_text, str) or not (10 <= len(message_text) <= 100):
        return False, "MessageText must be a string between 10 and 100 characters"
    
    try:
        datetime.strptime(event["messageDatetime"], "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return False, "Invalid datetime format"

    return True, None

def lambda_handler(event, context):
    try:
        body = json.loads(event['body']) if 'body' in event else event
        is_valid, error = validate_message(body)

        if not is_valid:
            return {"statusCode": 400, "body": json.dumps({"error": error})}

        table.put_item(Item=body)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Message stored successfully"})
        }

    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error"})
        }
