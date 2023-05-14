from pydantic import BaseModel, Field
from datetime import date
from typing import List, Optional

class LoginSchema(BaseModel):
    login: str = Field(title="Login")
    password: str = Field(title="Password")

class CurrentUserResponseModel(BaseModel):
    first_name: str = Field(title="First Name")
    last_name: str = Field(title="Last Name")
    other_name: str = Field(title="Other Name")
    email: str = Field(title="Email")
    phone: str = Field(title="Phone")
    birthday: str = Field(title="Birthday")
    is_admin: bool = Field(title="Is Admin")

class ErrorResponseModel(BaseModel):
    code: int = Field(title="Code")
    message: str = Field(title="Message")

class ValidationError(BaseModel):
    location: List[str] = Field(title="Location")
    msg: str = Field(title="Message")
    type: str = Field(title="Error Type")

class HTTPValidationError(BaseModel):
    detail: List[ValidationError] = Field(title="Detail")

class CodelessErrorResponseModel(BaseModel):
    message: str = Field(title="Message")

class UpdateUserModel(BaseModel):
    id: int = Field(title="Id")
    first_name: str = Field(title="First Name")
    last_name: str = Field(title="Last Name")
    other_name: str = Field(title="Other Name")
    email: str = Field(title="Email")
    phone: str = Field(title="Phone")
    birthday: date = Field(title="Birthday")

class UpdateUserResponseModel(BaseModel):
    id: int = Field(title="Id")
    first_name: str = Field(title="First Name")
    last_name: str = Field(title="Last Name")
    other_name: str = Field(title="Other Name")
    email: str = Field(title="Email")
    phone: str = Field(title="Phone")
    birthday: date = Field(title='Birthday')

class PaginatedMetaDataModel(BaseModel):
    total: int = Field(title="Total")
    page: int = Field(title="Page")
    size: int = Field(title="Size")

class UsersListMetaDataModel(BaseModel):
    pagination: PaginatedMetaDataModel

class UsersListElementModel(BaseModel):
    id: int = Field(title="Id")
    first_name: str = Field(title="First Name")
    last_name: str = Field(title="Last Name")
    email: str = Field(title="Email")

class UserListResponseModel(BaseModel):
    data: List[UsersListElementModel]
    meta: UsersListMetaDataModel

class CitiesHintModel(BaseModel):
    id: int = Field(title="Id")
    name: str = Field(title="Name")

class PrivateUsersListHintMetaModel(BaseModel):
    city: List[CitiesHintModel] = Field(title="City")

class PrivateUsersListMetaDataModel(BaseModel):
    pagination: PaginatedMetaDataModel
    hint: PrivateUsersListHintMetaModel

class PrivateUsersListResponseModel(BaseModel):
    data: List[UsersListElementModel] = Field(title="Data")
    meta: PrivateUsersListMetaDataModel

class PrivateDetailUserResponseModel(BaseModel):
    id: int = Field(title="Id")
    first_name: str = Field(title="First Name")
    last_name: str = Field(title="Last Name")
    other_name: str = Field(title="Other Name")
    email: str = Field(title="Email")
    phone: str = Field(title="Phone")
    birthday: str = Field(title="Birthday")
    city: int = Field(title="City")
    additional_info: str = Field(title="Additional Info")
    is_admin: bool = Field(title="Is Admin")

class PrivateUpdateUserModel(BaseModel):
    id: int = Field(title="Id")
    first_name: Optional[str] = Field(title="First Name")
    last_name: Optional[str] = Field(title="Last Name")
    other_name: Optional[str] = Field(title="Other Name")
    email: Optional[str] = Field(title="Email")
    phone: Optional[str] = Field(title="Phone")
    birthday: Optional[date] = Field(title="Birthday")
    city: Optional[int] = Field(title="City")
    additional_info: Optional[str] = Field(title="Additional Info")
    is_admin: Optional[bool] = Field(title="Is Admin")

class PrivateCreateUserModel(BaseModel):
    first_name: str = Field(title="First Name")
    last_name: str = Field(title="Last Name")
    other_name: Optional[str] = Field(title="Other Name")
    email: str = Field(title="Email")
    phone: Optional[str] = Field(title="Phone")
    birthday: Optional[date] = Field(title="Birthday")
    city: Optional[int] = Field(title="City")
    additional_info: Optional[str] = Field(title="Additional Info")
    is_admin: bool = Field(title="Is Admin")
    password: str = Field(title="Password")

