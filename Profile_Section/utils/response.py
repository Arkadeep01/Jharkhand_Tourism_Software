from fastapi.responses import JSONResponse
from fastapi import status
from typing import Any, Dict, Optional


def success_response(
    data: Any = None,
    message: str = "Success",
    status_code: int = status.HTTP_200_OK,
) -> JSONResponse:
    """
    Standard response for successful operations.
    """
    response_content: Dict[str, Any] = {"success": True, "message": message}
    if data is not None:
        response_content["data"] = data
    return JSONResponse(status_code=status_code, content=response_content)


def error_response(
    message: str = "An error occurred",
    status_code: int = status.HTTP_400_BAD_REQUEST,
    details: Optional[Any] = None,
) -> JSONResponse:
    """
    Standard response for errors.
    """
    response_content: Dict[str, Any] = {"success": False, "message": message}
    if details is not None:
        response_content["details"] = details
    return JSONResponse(status_code=status_code, content=response_content)


def not_found_response(
    message: str = "Resource not found",
) -> JSONResponse:
    """
    Shortcut for 404 responses.
    """
    return error_response(message=message, status_code=status.HTTP_404_NOT_FOUND)


def unauthorized_response(
    message: str = "Unauthorized",
) -> JSONResponse:
    """
    Shortcut for 401 responses.
    """
    return error_response(message=message, status_code=status.HTTP_401_UNAUTHORIZED)


def forbidden_response(
    message: str = "Forbidden",
) -> JSONResponse:
    """
    Shortcut for 403 responses.
    """
    return error_response(message=message, status_code=status.HTTP_403_FORBIDDEN)
