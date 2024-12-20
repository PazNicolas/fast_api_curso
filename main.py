from fastapi import Depends, FastAPI, Body, HTTPException, Path, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel
from models.user import User as UserModel
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
import bcrypt

app = FastAPI()
app.title = "Api Movies Nico"
app.version = "1.0.0"
templates = Jinja2Templates(directory="templates")

Base.metadata.create_all(bind=engine)

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales son invalidas")

class User(BaseModel):
    email:str
    password:str

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=100)
    overview: str = Field(min_length=10, max_length=2000)
    year: int = Field(le=2023)
    rating:float = Field(ge=1, le=10)
    category:str = Field(min_length=5, max_length=600)

    class Config:
        schema_extra = {
            "example": {
                "title": "Mi película",
                "overview": "Descripción de la película",
                "year": 2022,
                "rating": 9.8,
                "category" : "Acción"
            }
        }


@app.get('/', tags=['home'])
def message(request: Request):
    sections = [
        {'name': 'Películas', 'url': '/movies/1/'}
    ]
    return templates.TemplateResponse("index.html", {"request": request, "sections": sections})


@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)

@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': 'La pelicula no existe'})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    if not result:
        return JSONResponse(status_code=404, content={'message': 'No hay peliculas con esa categoria'})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la película"})

@app.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = db.query(MovieModel).get(id)
    if not result:
        return {'message': 'La pelicula no existe'}
    result.title, result.overview, result.year, result.rating, result.category = (
        movie.title, movie.overview, movie.year, movie.rating, movie.category
    )
    db.commit()
    return {'message': 'La pelicula ha sido actualizada'}

@app.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        raise HTTPException(status_code=404, detail='La pelicula no existe')
    db.delete(result)
    db.commit()
    return {'message': 'La pelicula ha sido eliminada'}

@app.post('/users', tags=['users'], response_model=dict, status_code=201)
def create_user(user: User) -> dict:
    db = Session()
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    new_user = UserModel(email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    return JSONResponse(status_code=201, content={"message": "Usuario creado"})

@app.get('/users', tags=['users'], response_model=List[User], status_code=200)
def get_users() -> List[User]:
    db = Session()
    result = db.query(UserModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.get('/users/{id}', tags=['users'], response_model=User)
def get_user(id: int = Path(ge=1, le=2000)) -> User:
    db = Session()
    result = db.query(UserModel).filter(UserModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': 'El usuario no existe'})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.put('/users/{id}', tags=['users'], response_model=dict, status_code=200)
def update_user(id: int, user: User) -> dict:
    db = Session()
    result = db.query(UserModel).get(id)
    if not result:
        return {'message': 'El usuario no existe'}
    result.email = user.email
    result.password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db.commit()
    return {'message': 'El usuario ha sido actualizado'}

@app.delete('/users/{id}', tags=['users'], response_model=dict, status_code=200)
def delete_user(id: int) -> dict:
    db = Session()
    result = db.query(UserModel).filter(UserModel.id == id).first()
    if not result:
        raise HTTPException(status_code=404, detail='El usuario no existe')
    db.delete(result)
    db.commit()
    return {'message': 'El usuario ha sido eliminado'}
