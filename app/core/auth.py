from datetime import timedelta

from authx import AuthX, AuthXConfig

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY

config = AuthXConfig()
config.JWT_ALGORITHM = ALGORITHM
config.JWT_SECRET_KEY = SECRET_KEY
config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))


security = AuthX(config=config)
