from typing import Any, Optional, Dict
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def standard_response(
    data: Any = None, 
    message: str = "Success", 
    code: str = "SUCCESS", 
    status_code: int = 200
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder({
            "code": code,
            "message": message,
            "data": data
        })
    )
