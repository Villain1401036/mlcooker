import sys
from fastapi import FastAPI
from parseresume import parse_resume
from pydantic import BaseModel

version = f"{sys.version_info.major}.{sys.version_info.minor}"

app = FastAPI()

class Processdata(BaseModel):
    resume_url: str
    description: str | None = None
    price: float | None = None
    tax: float | None = None

@app.post("/testbaby")
async def read_root(item :Processdata):
    item_data = item.dict()
    print(item_data)
    message = parse_resume(item_data["resume_url"])
    return message

@app.get("/")
async def read_root():
    message = f"Hello world! From FastAPI running on Uvicorn with Gunicorn. Using Python {version}"
    return {"message": message}
