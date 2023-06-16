from fastapi import HTTPException
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Optional

from starlette.requests import Request
# Se crea clase Movie, que hereda de BaseModel
from jwt_manager import validate_token
from fastapi.security import HTTPBearer


class User(BaseModel):
    email: str
    password: str


class Movie(BaseModel):
    id: Optional[int] = None  # Otra forma
    # id: int | None = None # Una forma de definir que es opcional
    title: str = Field(max_length=15, min_length=5)
    overview: str = Field(max_length=50, min_length=6)
    year: int = Field(le=2023)
    rating: float = Field(ge=2)
    category: str = Field(min_length=3, max_length=15)

    class Config:
        schema_extra = {
            "example": {
                'id': 1,
                'title': 'Name of a movie!',
                'overview': "A description of a movie!",
                'year': 2000,
                'rating': 10,
                'category': 'Action'
            }
        }


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
       auth = await super().__call__(request)
       data = validate_token(auth.credentials)
       if data['email'] != 'admin@admin.com':
           raise HTTPException(status_code=403, detail="Invalid credentials")
