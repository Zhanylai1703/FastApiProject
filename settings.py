from fastapi_users.authentication import (
    CookieTransport,
    AuthenticationBackend,
    JWTStrategy
)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from passlib.context import CryptContext


cookie_transport = CookieTransport(cookie_name='nashol', cookie_max_age=3600)


SECRET_KEY = "D46BC9A8C9D595548E6FD228DA152"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
