from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

class Item(BaseModel):
    name: str
    descriptijon: str | None = None
    price: float
    tax: float | None = None

fake_db = []

# GET
@app.get("/v1/items")
async def list_items():
    print(fake_db)
    return fake_db

@app.get("/v1/item")
async def get_item(id: int=0):
    print(fake_db[id])
    return fake_db[id]

# POST
@app.post("/v1/items")
async def create_item(item: Item):
    item_dict = item.model_dump()
    fake_db.append(item_dict)
    return item

# PUT

# DELETE