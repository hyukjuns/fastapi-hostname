from fastapi import FastAPI

app = FastAPI()

# GET
@app.get("/")
async def home():
    return {"Hello": "World"}