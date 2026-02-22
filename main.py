from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from config import settings
from api.api import router as api_router


Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #домены
    allow_credentials=True, #токены
    allow_methods=["*"], 
    allow_headers=["*"], 
)

app.include_router(api_router, prefix="/api")

@app.get("/")
def root():
    return {
        "message": "FastAPI Blog"
             }

