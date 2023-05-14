from fastapi import APIRouter, Response, Request, HTTPException, Query
from sqlalchemy.orm import Session

from ..models import engine, User
from ..schemas import (
    CurrentUserResponseModel, 
    ErrorResponseModel, 
    CodelessErrorResponseModel,
    UpdateUserModel, 
    UpdateUserResponseModel, 
    HTTPValidationError,
    UserListResponseModel,
    UserListElementModel, 
    UserListMetaDataModel,
    PaginatedMetaDataModel)

users_router = APIRouter(prefix='/users')

@users_router.get('/current', response_model=CurrentUserResponseModel, responses={
    400: {"model": ErrorResponseModel, "description": "Bad Request"},
    401: {"model": CodelessErrorResponseModel, "description": "Unauthorized"}},
    tags=["user"], summary="Получение данных о текущем пользователе", description="Здесь находится вся информация, доступная пользователю о самом себе, а так же информация является ли он администратором", operation_id="current_user_users_current_get")
def get_current_user(request: Request,response: Response):
    if not request.cookies.get('activeSession'):
        raise HTTPException(status_code=401, detail="Unauthorized")

    coockied_user = request.cookies.get('activeSession')
    with Session(bind=engine) as db:
        user = db.query(User).filter(User.login == coockied_user).one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="Bad Request")
    
    return CurrentUserResponseModel(first_name=user.first_name, last_name=user.last_name, other_name=user.other_name, email=user.email,phone=user.phone,birthday=user.birthday, is_admin=user.is_admin)
    


@users_router.patch('/current', response_model=UpdateUserResponseModel,responses={
    400: {"model": ErrorResponseModel,  "description": "Bad Request"},
    401: {"model": CodelessErrorResponseModel, "description": "Unauthorized"},
    404: {"model": CodelessErrorResponseModel, "description": "Not Found"},
    422: {"model": HTTPValidationError, "description": "Validation Error"}},
    tags=["user"], summary="Изменение данных пользователя", description="Здесь пользователь имеет возможность изменить свои данные", operation_id="edit_user_users__pk__patch")
def patch_current_user(request: Request, data: UpdateUserModel):
    if not request.cookies.get('activeSession'):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    coockied_user = request.cookies.get('activeSession')
    with Session(bind=engine) as db:
        user = db.query(User).filter(User.login == coockied_user).one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="Not Found")
        elif user:
            user.first_name = data.first_name
            user.last_name = data.last_name
            user.other_name = data.other_name
            user.email = data.email
            user.phone = data.phone
            user.birthday = data.birthday
            db.commit()
            return UpdateUserResponseModel(id=user.pk, first_name=user.first_name, last_name=user.last_name, other_name=user.other_name, email=user.email, phone=user.phone, birthday=user.birthday)
    raise HTTPException(status_code=400, detail="Bad Request")

@users_router.get("/",response_model=UserListResponseModel, responses={
    400: {"model": ErrorResponseModel,  "description": "Bad Request"},
    401: {"model": CodelessErrorResponseModel, "description": "Unauthorized"},
    422: {"model": HTTPValidationError, "description": "Validation Error"}},
    tags=["user"], summary="Постраничное получение кратких данных обо всех пользователях",
    description="Здесь находится вся информация, доступная пользователю о других пользователях",
    operation_id="users_users_get")
def get_users(request: Request, page: int = Query(..., title="Page", gt=0), size: int = Query(..., title="Size", gt=0)):
    if not request.cookies.get("activeSession"):
        raise HTTPException(status_code=401, detail="Unauthorized")
    with Session(bind=engine) as db:
        users = db.query(User).offset((page - 1)*size).limit(size).all()
        total = db.query(User).count()

    return UserListResponseModel(data=[UserListElementModel(
                                    id=user.pk, 
                                    first_name=user.first_name, 
                                    last_name=user.last_name, 
                                    email=user.email) for user in users], 
                                meta=UserListMetaDataModel(
                                    pagination=PaginatedMetaDataModel(
                                    total=total, 
                                    page=page, 
                                    size=size)))
