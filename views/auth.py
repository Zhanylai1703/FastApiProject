from datetime import timedelta
from fastapi import HTTPException, status, Depends, APIRouter

from sqlalchemy.orm import Session

from settings import ACCESS_TOKEN_EXPIRE_MINUTES, oauth2_scheme
from models.models import User
from shcemas.shemas import UserIn, Token, LoginModel, NewPassword
from core.db import get_db, get_password_hash, pwd_context
from managers.auth import create_access_token

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.requests import Request
import jwt

router = APIRouter(
    prefix='/users',
    tags=['Auth']
)


class EmailPasswordOAuth2PasswordBearer(OAuth2PasswordBearer):
    async def __call__(self, request: Request):
        form = await request.form()
        username = form.get("email")
        password = form.get("password")

        if username and password:
            return OAuth2PasswordRequestForm(
                password=password,
            )

        return await super().__call__(request)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email).first()

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    new_user = User(
        email=user_in.email,
        password=get_password_hash(user_in.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users", status_code=status.HTTP_200_OK)
async def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.post("/login", response_model=Token)
async def login(login: LoginModel = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login.email).first()

    if not user or not pwd_context.verify(login.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.put("/change-password", status_code=status.HTTP_201_CREATED)
async def change_password(current_password: str, new_password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == current_user_email).first()
    if not user or not pwd_context.verify(current_password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    user.password = get_password_hash(new_password)
    db.commit()

    return {"message": "Password changed successfully"}


@router.get("/protected", dependencies=[Depends(oauth2_scheme)])
async def protected_endpoint():
    return {"message": "This is a protected endpoint"}
