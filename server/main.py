from typing import Union
from fastapi import FastAPI

# Corrected Imports
from database import engine, Base
from schemas.schema import Item
from models.user import User

Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

# Added the missing @ and corrected the path
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# Added the missing @ and leading slash
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name}