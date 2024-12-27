from authx.exceptions import JWTDecodeError
from fastapi import Request
from fastapi.responses import JSONResponse


async def jwt_decode_error_handler(request: Request, exc: JWTDecodeError) -> JSONResponse:
    """
    Обработчик ошибок для JWT токенов.
    Этот обработчик вызывается, когда происходит ошибка декодирования JWT токена (например, токен истек или недействителен).
    Он возвращает ответ с ошибкой 401 и подробным сообщением о том, что токен истек или является недействительным.
    """
    return JSONResponse(
        status_code=401,
        content={"detail": "Token has expired or is invalid. Please log in again."},
    )
