from fastapi import APIRouter, Request, Query, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash

from ..models import User, City, engine
from ..schemas import (
    UsersListElementModel,
    PrivateUsersListResponseModel,
    PrivateUsersListMetaDataModel,
    PaginatedMetaDataModel,
    PrivateUsersListHintMetaModel,
    CitiesHintModel,
    ErrorResponseModel,CodelessErrorResponseModel,
    HTTPValidationError,
    PrivateDetailUserResponseModel,
    PrivateCreateUserModel,
    PrivateUpdateUserModel)


admin_router = APIRouter(prefix='/private')

@admin_router.get('/users', response_model=PrivateUsersListResponseModel, responses={
    400: {"model": ErrorResponseModel,  "description": "Bad Request"},
    401: {"model": CodelessErrorResponseModel, "description": "Unauthorized"},
    403: {"model": CodelessErrorResponseModel, "description": "Forbidden"},
    422: {"model": HTTPValidationError, "description": "Validation Error"}},
    tags=["admin"], summary="Постраничное получение кратких данных обо всех пользователях",
    description="Здесь находится вся информация, доступная пользователю о других пользователях",
    operation_id="private_users_private_users_get"
)
def admin_get_users(request: Request, page: int = Query(..., title="Page", gt=0), size: int = Query(..., title="Size", gt=0)):
    if not request.cookies.get("activeSession"):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    if request.cookies.get("isAdmin") == False:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    with Session(bind=engine) as db:
        users = db.query(User).offset((page - 1)*size).limit(size).all()
        total = db.query(User).count()
        cities = db.query(City).all()

    return PrivateUsersListResponseModel(data=[UsersListElementModel(
                                    id=user.pk, 
                                    first_name=user.first_name, 
                                    last_name=user.last_name, 
                                    email=user.email) for user in users], 
                                meta=PrivateUsersListMetaDataModel(
                                    pagination=PaginatedMetaDataModel(
                                    total=total, 
                                    page=page, 
                                    size=size),
                                hint=PrivateUsersListHintMetaModel(
                                    city=[CitiesHintModel(id=city.id, name=city.name) for city in cities])))

@admin_router.post("/users", response_model=PrivateDetailUserResponseModel, responses={
    400: {"model": ErrorResponseModel, "description": "Bad Request"},
    401: {"model": CodelessErrorResponseModel, "description": "Unauthorized"},
    403: {"model": CodelessErrorResponseModel, "description": "Forbidden"},
    422: {"model": HTTPValidationError, "description": "Validation Error"}},
    tags=["admin"], summary="Создание пользователя", 
    description="Здесь возможно занести в базу нового пользователя с минимальной информацией о нем",
    operation_id="private_create_users_private_users_post")
def create_users(data: PrivateCreateUserModel, request: Request):
    if not request.cookies.get("activeSession"):
        raise HTTPException(status_code=401, detail="Unauthorized")
    if request.cookies.get("isAdmin") == False:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    dict_data = data.dict()
    new_user = User(**dict_data)
    with Session(engine) as db:
        db.add(new_user)
        db.commit()
        
        return PrivateDetailUserResponseModel(**dict_data)
    
@admin_router.get("/users/{id}", response_model=PrivateDetailUserResponseModel, responses={
    400: {"model": ErrorResponseModel,  "description": "Bad Request"},
    401: {"model": CodelessErrorResponseModel, "description": "Unauthorized"},
    403: {"model": CodelessErrorResponseModel, "description": "Forbidden"},
    404: {"model": CodelessErrorResponseModel, "description": "Not Found"},
    422: {"model": HTTPValidationError, "description": "Validation Error"}},
    tags=["admin"],summary="Детальное получение информации о пользователе",
    description="Здесь администратор может увидеть всю существующую пользовательскую информацию",
    operation_id="private_get_user_private_users__pk__get")
def get_user_by_id(id, request: Request):
    if not request.cookies.get("activeSession"):
        raise HTTPException(status_code=401, detail="Unauthorized")
    if request.cookies.get("isAdmin") == False:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    with Session(bind=engine) as db:
        user = db.query(User).filter(User.pk == id).one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="Not Found")
        
        return PrivateDetailUserResponseModel(id=user.pk,
                                              first_name=user.first_name,
                                              last_name=user.last_name,
                                              other_name=user.other_name,
                                              email=user.email,
                                              phone=user.phone,
                                              birthday=user.birthday,
                                              city=user.city,
                                              additional_info=user.additional_info,
                                              is_admin=user.is_admin)

@admin_router.delete("/users/{id}", responses={
    401: {"model": CodelessErrorResponseModel, "description": "Unauthorized"},
    403: {"model": CodelessErrorResponseModel, "description": "Forbidden"},
    404: {"model": CodelessErrorResponseModel, "description": "Not Found"},
    422: {"model": HTTPValidationError, "description": "Validation Error"}},
    tags=["admin"],summary="Удаление пользователя",
    description="Удаление пользователя",
    operation_id="private_delete_user_private_users__pk__delete")
def delete_user_by_id(id, request: Request):
    if not request.cookies.get("activeSession"):
        raise HTTPException(status_code=401, detail="Unauthorized")
    if request.cookies.get("isAdmin") == False:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    with Session(bind=engine) as db:
        user = db.query(User).filter(User.pk == id).one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="Not Found")
        db.delete(user)
        db.commit()
        return JSONResponse(status_code=204, content="Successful Response")
    
@admin_router.patch("/users/{id}", response_model=PrivateDetailUserResponseModel, responses={
    401: {"model": CodelessErrorResponseModel, "description": "Unauthorized"},
    403: {"model": CodelessErrorResponseModel, "description": "Forbidden"},
    404: {"model": CodelessErrorResponseModel, "description": "Not Found"},
    422: {"model": HTTPValidationError, "description": "Validation Error"}},
    tags=["admin"],summary="Изменение информации о пользователе",
    description="Здесь администратор может изменить любую информацию о пользователе",
    operation_id="private_patch_user_private_users__pk__patch")
def patch_user_info_by_id(id, request: Request, data: PrivateUpdateUserModel):
    if not request.cookies.get("activeSession"):
        raise HTTPException(status_code=401, detail="Unauthorized")
    if request.cookies.get("isAdmin") == False:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    with Session(bind=engine) as db:
        user = db.query(User).filter(User.pk == id).one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="Not Found")
        dict_data = data.dict()
        return PrivateDetailUserResponseModel(**dict_data)
    

