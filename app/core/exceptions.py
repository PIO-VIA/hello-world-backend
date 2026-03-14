from typing import Any, Optional
from fastapi import HTTPException, status

class AppException(HTTPException):
    def __init__(
        self, 
        message: str, 
        code: str, 
        status_code: int = status.HTTP_400_BAD_REQUEST,
        data: Optional[Any] = None
    ):
        super().__init__(status_code=status_code, detail={"message": message, "code": code, "data": data})

class AuthenticationError(AppException):
    def __init__(self, message: str = "Authentication failed", code: str = "AUTH_ERROR", data: Optional[Any] = None):
        super().__init__(message, code, status.HTTP_401_UNAUTHORIZED, data)

class PermissionDeniedError(AppException):
    def __init__(self, message: str = "Permission denied", code: str = "PERMISSION_DENIED", data: Optional[Any] = None):
        super().__init__(message, code, status.HTTP_403_FORBIDDEN, data)

class NotFoundError(AppException):
    def __init__(self, message: str = "Resource not found", code: str = "NOT_FOUND", data: Optional[Any] = None):
        super().__init__(message, code, status.HTTP_404_NOT_FOUND, data)

class ValidationError(AppException):
    def __init__(self, message: str = "Validation error", code: str = "VALIDATION_ERROR", data: Optional[Any] = None):
        super().__init__(message, code, status.HTTP_422_UNPROCESSABLE_ENTITY, data)
