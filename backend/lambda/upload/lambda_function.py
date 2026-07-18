from handlers import (
    health_response,
    upload_url_response,
    upload_response,
    list_documents_response,
    get_document_response,
    delete_document_response,
)

from utils import build_response


def lambda_handler(event, context):

    route_key = event.get("routeKey")

    if route_key == "GET /health":
        return health_response()

    if route_key == "GET /documents":
        return list_documents_response(event)    

    if route_key == "GET /documents/{document_id}":
        return get_document_response(event)    
    
    if route_key == "DELETE /documents/{document_id}":
        return delete_document_response(event)

    if route_key == "POST /upload-url":
        return upload_url_response(event)

    if route_key == "POST /upload":
        return upload_response(event)

    return build_response(
        404, 
        {
            "success": False,
            "message": "Route not found"
        }
    )