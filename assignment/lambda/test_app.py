import os
import json
import pytest

os.environ["TABLE_NAME"] = "Messages"
from app import lambda_handler

print(f'TABLE_NAME environment variable is set to: {os.environ["TABLE_NAME"]}')

def test_valid_message():
    event = {
        "body": json.dumps({
            "messageUUID": "12345",
            "messageText": "This is a valid message",
            "messageDatetime": "2024-02-01 10:00:00"
        })
    }
    context = {}
    response = lambda_handler(event, context)

    assert response['statusCode'] == 200
    assert json.loads(response['body'])["message"] == "Message stored successfully"
