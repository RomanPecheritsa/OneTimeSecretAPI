import jwt
from fastapi import Depends, HTTPException
from starlette import status

from app.core.config import ALGORITHM, SECRET_KEY
from app.users.routes import oauth2_scheme


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Извлекает текущего пользователя из JWT-токена.

    Данная функция используется для аутентификации пользователя, декодируя JWT-токен,
    получая из него имя пользователя и проверяя его валидность. В случае истечения срока
    действия токена или если токен является некорректным, выбрасывается HTTP исключение с
    соответствующим статусом.

    :param token: JWT токен, передаваемый через заголовок Authorization.
    :return: Имя пользователя (строка), если токен действителен.
    :raises HTTPException: В случае ошибок с токеном (истек, некорректный токен).
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username = payload.get("sub")

        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
