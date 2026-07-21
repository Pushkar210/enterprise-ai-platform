from datetime import datetime, timezone
import mimetypes
import os

import boto3

s3_client = boto3.client("s3")

documents_table = boto3.resource("dynamodb").Table(
    os.environ["DOCUMENTS_TABLE_NAME"]
)

document_bucket = os.environ["BUCKET_NAME"]


def generate_upload_url(document_id, filename):
    object_key = f"documents/{document_id}/{filename}"

    content_type, _ = mimetypes.guess_type(filename)

    if content_type is None:
        content_type = "application/octet-stream"

    upload_url = s3_client.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket": document_bucket,
            "Key": object_key,
            "ContentType": content_type
        },
        ExpiresIn=600
    )

    return {
        "object_key": object_key,
        "upload_url": upload_url
    }


def save_document_metadata(document_id, filename, object_key):
    s3_client.head_object(
        Bucket=document_bucket,
        Key=object_key
    )

    created_at = datetime.now(timezone.utc).isoformat()

    document_item = {
        "document_id": document_id,
        "filename": filename,
        "object_key": object_key,
        "status": "uploaded",
        "created_at": created_at
    }

    documents_table.put_item(Item=document_item)

    return document_item


def list_documents():
    response = documents_table.scan()

    return {
        "count": response.get("Count", 0),
        "documents": response.get("Items", [])
    }


def get_document(document_id):
    response = documents_table.get_item(
        Key={
            "document_id": document_id
        }
    )

    return response.get("Item")


def delete_document(document_id):
    response = documents_table.get_item(
        Key={
            "document_id": document_id
        }
    )

    item = response.get("Item")

    if not item:
        return False

    s3_client.delete_object(
        Bucket=document_bucket,
        Key=item["object_key"]
    )

    documents_table.delete_item(
        Key={
            "document_id": document_id
        }
    )

    return True

def ask_document(document_id, question):
    document = get_document(document_id)

    if not document:
        return None

    return {
        "document": document,
        "question": question
    }