import json
import os
import uuid
from datetime import datetime, timezone

import boto3


dynamodb = boto3.resource("dynamodb")
documents_table = dynamodb.Table(os.environ["DOCUMENTS_TABLE_NAME"])

s3_client = boto3.client("s3")
bucket_name = os.environ["BUCKET_NAME"]


def build_response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }


def health_response():
    return build_response(200, {
        "success": True,
        "message": "Lambda is running successfully",
        "environment": os.environ["ENVIRONMENT"],
        "service": "enterprise-ai-platform",
        "version": "1.0.0"
    })

def generate_upload_url(document_id, filename):
    object_key = f"documents/{document_id}/{filename}"

    upload_url = s3_client.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket": bucket_name,
            "Key": object_key,
            "ContentType": "application/pdf"
        },
        ExpiresIn=600
    )

    return {
        "object_key": object_key,
        "upload_url": upload_url
    }

def upload_response(event):
    document_id = str(uuid.uuid4())
    created_at = datetime.now(timezone.utc).isoformat()

    try:
        body = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return build_response(400, {
            "success": False,
            "message": "Invalid JSON body"
        })

    filename = body.get("filename")

    if not filename or not filename.strip():
        return build_response(400, {
            "success": False,
            "message": "filename is required"
        })

    document_item = {
        "document_id": document_id,
        "filename": filename,
        "status": "received",
        "created_at": created_at
    }

    documents_table.put_item(Item=document_item)

    return build_response(201, {
        "success": True,
        "message": "Document metadata saved",
        "document": document_item
    })

def upload_url_response(event):
    document_id = str(uuid.uuid4())

    try:
        body = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return build_response(400, {
            "success": False,
            "message": "Invalid JSON body"
        })

    filename = body.get("filename")

    if not filename or not filename.strip():
        return build_response(400, {
            "success": False,
            "message": "filename is required"
        })

    upload_details = generate_upload_url(document_id, filename)

    return build_response(200, {
        "success": True,
        "document_id": document_id,
        "filename": filename,
        "object_key": upload_details["object_key"],
        "upload_url": upload_details["upload_url"]
    })

def lambda_handler(event, context):
    route_key = event.get("routeKey")

    if route_key == "GET /health":
        return health_response()

    if route_key == "POST /upload":
        return upload_response(event)

    if route_key == "POST /upload-url":
        return upload_url_response(event)

    return build_response(404, {
        "success": False,
        "message": "Route not found"
    })