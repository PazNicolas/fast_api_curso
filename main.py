from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Body

app = FastAPI()
app.title = "Api de Nico"
app.version = "1.0"


class Movie(BaseModel):
    id: Optional[int] = None
    title: str
    overview: str
    year: int
    rating: float
    category: str
    category: str


movies = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        "year": "2009",
                "rating": 7.8,
                "category": "Acción"
    },

    {
        "id": 2,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        "year": "2009",
                "rating": 7.8,
                "category": "Acción"
    }
]


@app.get('/movies', tags=['movies'])
def get_movies():
    return movies


@app.get("/movies/{id}", tags=["Movies"])
def get_movie(id: int):
    for item in movies:
        if item["id"] == id:
            return item
    raise HTTPException(status_code=404, detail="Pelicula no encontrada")


@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str, year: int):
    return [item for item in movies if item['category'] == category]


@app.post('/movies', tags=['movies'])
def create_movie(movie: Movie):
    movies.append(movie)
    return movies


@app.put('/movies/{id}', tags=['movies'])
def update_movie(id: int, movie: Movie):
    for mov in movies:
        if mov["id"] == id:
            mov.update(movie)
    return movies


@app.delete('/movies/{id}', tags=['movies'])
def delete_movie(id: int):
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return movies
