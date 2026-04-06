from fastapi import Depends, status, APIRouter
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated

from app.models.user import User
from app.schema import UserResponse
from app.dependecies import get_current_user
from app.database import get_session

router = APIRouter()
auth2_chema = OAuth2PasswordBearer(tokenUrl="./login")

@router.get("/me")
def get_user(user: Annotated[User, Depends(get_current_user)]):
    return UserResponse(name=user.name, email=user.email, is_verified=user.is_verified)

@router.delete("/delete-account")
def delete_account(user: Annotated[User, Depends(get_current_user)], session : Annotated[Session, Depends(get_session)]):
    session.query(User).filter_by(email=user.email).delete()
    session.commit()
    return {"message":"Your account is successfully deleted", "status":status.HTTP_200_OK}