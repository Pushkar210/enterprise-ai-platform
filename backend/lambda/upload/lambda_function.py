import json


def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "success": True,
            "message": "Lambda is running successfully",
            "environment": "dev",
            "service": "enterprise-ai-platform",
            "version": "1.0.0"
        })
    }