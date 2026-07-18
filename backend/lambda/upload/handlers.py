import json
import os
import uuid

from services import (
    generate_upload_url,
    save_document_metadata,
    list_documents,
    get_document,
    delete_document,
)
from utils import build_response


def health_response():
    return build_response(200, {
        "success": True,
        "message": "Lambda is running successfully",
        "environment": os.environ["ENVIRONMENT"],
        "service": "enterprise-ai-platform",
        "version": "1.0.0"
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


def upload_response(event):

    try:
        body = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return build_response(400, {
            "success": False,
            "message": "Invalid JSON body"
        })

    document_id = body.get("document_id")
    filename = body.get("filename")
    object_key = body.get("object_key")

    if not document_id or not filename or not object_key:
        return build_response(400, {
            "success": False,
            "message": "document_id, filename and object_key are required"
        })

    try:
        document = save_document_metadata(
            document_id,
            filename,
            object_key
        )

        return build_response(201, {
            "success": True,
            "message": "Document metadata saved",
            "document": document
        })

    except Exception as error:
        return build_response(400, {
            "success": False,
            "message": str(error)
        })


def list_documents_response(event):
    try:
        result = list_documents()

        return build_response(200, {
            "success": True,
            "count": result["count"],
            "documents": result["documents"]
        })

    except Exception as error:
        return build_response(500, {
            "success": False,
            "message": str(error)
        })

def get_document_response(event):

    path_parameters = event.get("pathParameters") or {}
    document_id = path_parameters.get("document_id")

    if not document_id:
        return build_response(400, {
            "success": False,
            "message": "document_id is required"
        })

    try:
        document = get_document(document_id)

        if not document:
            return build_response(404, {
                "success": False,
                "message": "Document not found"
            })

        return build_response(200, {
            "success": True,
            "document": document
        })

    except Exception as error:
        return build_response(500, {
            "success": False,
            "message": str(error)
        })

def delete_document_response(event):

    path_parameters = event.get("pathParameters") or {}
    document_id = path_parameters.get("document_id")

    if not document_id:
        return build_response(400, {
            "success": False,
            "message": "document_id is required"
        })

    try:
        deleted = delete_document(document_id)

        if not deleted:
            return build_response(404, {
                "success": False,
                "message": "Document not found"
            })

        return build_response(200, {
            "success": True,
            "message": "Document deleted successfully"
        })

    except Exception as error:
        return build_response(500, {
            "success": False,
            "message": str(error)
        })