from pydantic import BaseModel
from datetime import datetime
from typing import List

class LoginSchema(BaseModel):
    login: str
    password: str

class CurrentUserResponseModel(BaseModel):
    first_name: str
    last_name: str
    other_name: str
    email: str
    phone: str
    birthday: datetime
    is_admin: bool

class ErrorResponseModel(BaseModel):
    code: int
    message: str

class ValidationError(BaseModel):
    location: str
    msg: str
    type: str

class HTTPValidationError(BaseModel):
    detail: List[ValidationError]

class CodelessErrorResponseModel(BaseModel):
    message: str

class UpdateUserModel(BaseModel):
    first_name: str
    last_name: str
    other_name: str
    email: str
    phone: str
    birthday: datetime

class UpdateUserResponseModel(BaseModel):
    id: int
    first_name: str
    last_name: str
    other_name: str
    email: str
    phone: str
    birthday: datetime

class PaginatedMetaDataModel(BaseModel):
    total: int
    page: int
    size: int

class UserListMetaDataModel(BaseModel):
    pagination: PaginatedMetaDataModel

class UserListElementModel(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

class UserListResponseModel(BaseModel):
    data: List[UserListElementModel]
    meta: UserListMetaDataModel