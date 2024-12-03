from fastapi import FastAPI,Form
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import Annotated,List
from pydantic import BaseModel

class GameData(BaseModel):
    title: str
    description: str
    words: List[str]
    public: bool
app = FastAPI()

@app.post('/create-game')
def create_game(game_data: GameData):
    print(game_data.title,game_data.description,game_data.words,game_data.public)
    return '200'


app.mount("/",StaticFiles(directory="frontend",html=True),name="frontend")