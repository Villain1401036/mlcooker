import sys
from fastapi import FastAPI
from parseresume import parse_resume , download_pdf_from_link
from pydantic import BaseModel
from scripts.ResumeProcessor import ResumeProcessor 

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
    try:
        resume_path = download_pdf_from_link(item_data["resume_url"])
        if resume_path:
            print("Resume downloaded successfully:", resume_path)
        else:
            print("Failed to download the resume.")
        
        processor = ResumeProcessor(f'{resume_path}')
        data = processor.process() 
        return data

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {"error": str(e)}

@app.post("/resumeprocessor")
async def resumeprocessor(item :Processdata):
    item_data = item.dict()
    print(item_data)
    message = parse_resume(item_data["resume_url"])
    return message

@app.get("/")
async def read_root():
    message = f"Hello world! From FastAPI running on Uvicorn with Gunicorn. Using Python {version}"
    return {"message": message}
