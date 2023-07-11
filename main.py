from fastapi import FastAPI

from views.views import router as nashol_router
from views.auth import router as create_user, EmailPasswordOAuth2PasswordBearer


oauth2_scheme = EmailPasswordOAuth2PasswordBearer(tokenUrl="/auth")


app = FastAPI(
    title='Snake People',
    version = "1.0.0",
)


app.include_router(nashol_router)
app.include_router(create_user)
