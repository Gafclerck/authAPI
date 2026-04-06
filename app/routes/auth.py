from fastapi import Depends, HTTPException, status, APIRouter, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import timedelta

from app.models.user import User
from app.schema import RegistrationRequest, Token
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.security import create_access_token, hash_password, authenticate_user
from app.database import get_session

auth2_chema = OAuth2PasswordBearer(tokenUrl="./login")

router = APIRouter()

@router.post("/register")
def register(user : RegistrationRequest, db: Annotated[Session, Depends(get_session)]):
    hashed_password = hash_password(user.password)
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already registered"
        )
    db.add(User(name=user.name, email=user.email, password=hashed_password))
    db.commit()
    return {"message":"Successfully registered", "status":status.HTTP_201_CREATED}


@router.post("/login")
def login(form_data : Annotated[OAuth2PasswordRequestForm, Depends()], db : Annotated[Session, Depends(get_session)]):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Not Authenticated",
            headers={"WWW-Authenticate" : "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")