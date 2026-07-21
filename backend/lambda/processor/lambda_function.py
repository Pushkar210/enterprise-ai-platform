import json

from services import get_document, update_document


def lambda_handler(event, context):
    print("Received S3 event:")
    print(json.dumps(event, indent=2))

    record = event["Records"][0]

    bucket_name = record["s3"]["bucket"]["name"]
    object_key = record["s3"]["object"]["key"]
    document_id = object_key.split("/")[1]    

    document = get_document(bucket_name, object_key)

    print(f"Bucket: {document['bucket']}")
    print(f"Object: {document['object_key']}")
    print(f"File size: {document['file_size']} bytes")
    print("File content:")
    print(document["content"])

    update_document(
        document_id=document_id,
        content=document["content"]
    )

    print(f"Document {document_id} updated successfully.")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "success": True,
            "bucket": document["bucket"],
            "object_key": document["object_key"],
            "file_size": document["file_size"]
        })
    }