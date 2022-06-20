from typing import TypedDict
from pydantic import BaseModel

# --- User authorization ---

class AuthorizationDataModel(BaseModel):
    Login: str
    Password: str

class SuccessAuthorizationResponseModel(BaseModel):
    Token: str

class SuccessRegistrationResponseModel(BaseModel):
    Token: str

class TokenRequestBodyModel(BaseModel):
    Token: str

# --- Wishes ---

class WishesRequestBodyModel(BaseModel):
    Token: str
    Wish: str
    Target: int | None

class WishesWithoutTargetDatabaseModel(TypedDict):
    ID: int
    Wish: str
    Owner: int

class WishIDModel(BaseModel):
    ID: int

# --- Database ---

class UserInDatabaseModel(TypedDict):
    ID: int
    Login: str
    HashOfPassword: str

