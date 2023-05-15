from fastapi import APIRouter, Response, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import and_
from werkzeug.security import check_password_hash, generate_password_hash
from random import randint

from ..models import engine, User
from ..schemas import LoginSchema, CurrentUserResponseModel, ErrorResponseModel, HTTPValidationError, CodelessErrorResponseModel

login_router = APIRouter()

@login_router.post("/registration", tags=["auth"])
def register(data: LoginSchema):
    with Session(bind=engine) as db:
        new_user = User(login=data.login, hash_password=generate_password_hash(data.password))
        db.add(new_user)
        db.commit()
    return {'good?': "good"}


@login_router.post('/login', response_model=CurrentUserResponseModel, responses={
    400: {"model": ErrorResponseModel, "description": "Bad request"},
    422: {"model": HTTPValidationError, "description": "Validation Error"}},
    tags=["auth"], summary="Вход в систему", operation_id="login_login_post")
def login(response: Response, login_data: LoginSchema):
    with Session(bind=engine) as db:
        user = db.query(User).filter(and_(User.login == login_data.login)).one_or_none()
    if user:
        if check_password_hash(user.hash_password, login_data.password):
            response.set_cookie(key='activeSession', value=login_data.login)
            response.set_cookie(key='isAdmin', value=user.is_admin)
            return CurrentUserResponseModel(
                first_name=user.first_name,
                last_name=user.last_name,
                other_name=user.other_name,
                phone=user.phone,
                email=user.email,
                birthday=user.birthday,
                is_admin=user.is_admin
            )
        raise HTTPException(status_code=400, detail='Invalid password')
    raise HTTPException(status_code=400, detail='Invalid login')
        

@login_router.get('/logout', responses={
    200: {"description": "Successful Response"}},
    tags=["auth"], summary="Выход из системы", description="При успешном выходе необходимо удалить установленные Cookies", 
    operation_id="logout_logout_get")
def logout(response: Response, request: Request):
    if not request.cookies.get('activeSession') or not request.cookies.get("isAdmin"):
        return {"message": "You're already logged out"}
    response.delete_cookie(key='activeSession')
    response.delete_cookie(key='isAdmin')
    return {"description": "Successful Response"}