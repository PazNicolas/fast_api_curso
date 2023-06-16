from fastapi import FastAPI, HTTPException, Body, Depends, Request
from fastapi.responses import JSONResponse, HTMLResponse
from typing import Optional
from pydantic import BaseModel, Field
from data import movies
from models import Movie, User, JWTBearer
from jwt_manager import create_token


app = FastAPI()
app.title = "Api de Nico"
app.version = "1.0"


@app.get('/movies', tags=['Movies'])
def get_movies():
    return movies


@app.get("/movies/{id}", tags=["Movies"], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movie(id: int):
    for item in movies:
        if item["id"] == id:
            return item
    raise HTTPException(status_code=404, detail="Pelicula no encontrada")


@app.get('/movies/', tags=['Movies'])
def get_movies_by_category(category: str, year: int):
    return [item for item in movies if item['category'] == category]


@app.post('/movies', tags=['Movies'],status_code=201)
def create_movie(movie: Movie):
    movies.append(movie)
    return JSONResponse(status_code=201, content={"message": "Pelicula agregada"})


@app.put('/movies/{id}', tags=['Movies'],status_code=200)
def update_movie(id: int, movie: Movie):
    for mov in movies:
        if mov["id"] == id:
            mov.update(movie)
    return movies


@app.delete('/movies/{id}', tags=['Movies'], status_code=200)
def delete_movie(id: int):
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(status_code=204, content={"message": "Pelicula eliminada"})
        

@app.post('/login',tags=['Auth'])
def login(user: User):
    if user.email == "admin@admin.com" and user.password == "admin":
        token:str = create_token(user.dict())
    return JSONResponse(content=token, status_code=200)