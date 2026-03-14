from typing import Any, Optional, Dict
from fastapi.responses import JSONResponse

def standard_response(
    data: Any = None, 
    message: str = "Success", 
    code: str = "SUCCESS", 
    status_code: int = 200
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "code": code,
            "message": message,
            "data": data
        }
    )
