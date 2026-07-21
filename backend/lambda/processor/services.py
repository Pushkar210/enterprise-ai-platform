import os

import boto3

from extractors.pdf import extract_text as extract_pdf_text
from extractors.txt import extract_text as extract_txt_text

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table(os.environ["DOCUMENTS_TABLE_NAME"])

def get_document(bucket_name, object_key):
    response = s3.get_object(
        Bucket=bucket_name,
        Key=object_key
    )

    file_size = response["ContentLength"]
    file_bytes = response["Body"].read()

    extension = os.path.splitext(object_key)[1].lower()

    if extension == ".txt":
        content = extract_txt_text(file_bytes)

    elif extension == ".pdf":
        content = extract_pdf_text(file_bytes)

    else:
        raise ValueError(f"Unsupported file type: {extension}")

    return {
        "bucket": bucket_name,
        "object_key": object_key,
        "file_size": file_size,
        "content": content
    }


def update_document(document_id, content):
    table.update_item(
        Key={
            "document_id": document_id
        },
        UpdateExpression="""
            SET #status = :status,
                #content = :content
        """,
        ExpressionAttributeNames={
            "#status": "status",
            "#content": "content"
        },
        ExpressionAttributeValues={
            ":status": "processed",
            ":content": content
        }
    )