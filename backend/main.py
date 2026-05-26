from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from fastapi import UploadFile, File
import os

app = FastAPI()

# Upload directory
UPLOAD_DIR = "../uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

#cors config
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

llm = ChatOllama(model ="deepseek-coder")

class ChatRequest(BaseModel):
    message: str
    
@app.post("/chat")
async def chat(req: ChatRequest):
    response = llm.invoke(req.message)
    return{
        "response": response.content
    }

@app.get("/")
def home():
    return {"message":"AI coding Assistent Running"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    return {
        "message": "uploaded",
        "filename": file.filename
    }