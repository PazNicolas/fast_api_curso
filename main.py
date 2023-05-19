import db
from fastapi import FastAPI,HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = "Api de Nico"
app.version = "1.0"



@app.get("/", tags=["Home"])
def saludo():
    return HTMLResponse("<h1>Hello world</h1>")



@app.get("/movies/{id}",tags=["Movies"])
def get_movie(id: int):
    for item in db.data:
        if item["id"] == id:
            return item
    raise HTTPException(status_code=404, detail="Pelicula no encontrada") 


@app.get("/movies/", tags=["Movies"])
def get_movies_by_genres(genres: str, year: int):
    return genres