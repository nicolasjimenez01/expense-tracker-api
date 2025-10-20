from fastapi import APIRouter, Depends
from app.schemas import user_schema

from app.services import user_service, auth_service
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.token_schema import Token

router = APIRouter(prefix="/users")

@router.get("/")
def get_users():
    return user_service.list_users()

@router.post("/")
def create_user(data: user_schema.UserDb):
    return user_service.create_user(data)

@router.post(
    "/login",
    tags=["users"],
    response_model=Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    return auth_service.generate_token(form_data.username, form_data.password)

