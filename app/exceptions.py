from authx.exceptions import JWTDecodeError
from fastapi import Request
from fastapi.responses import JSONResponse


async def jwt_decode_error_handler(request, exc):
    return JSONResponse(
        status_code=401,
        content={"detail": "Token has expired or is invalid. Please log in again."},
    )
