from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.database import get_session
from jwt.exceptions import InvalidTokenError
from app.config import SECRET_KEY, ALGORITHM
from typing import Annotated
from sqlalchemy.orm import Session
import jwt
from app.models.user import User

auth2_chema = OAuth2PasswordBearer(tokenUrl="./login")

def get_current_user(token: Annotated[str, Depends(auth2_chema)], session : Annotated[Session, Depends(get_session)]) -> User:
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = session.query(User).filter(User.email == username).first()
    if user is None:
        raise credentials_exception
    return user
