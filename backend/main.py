from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import database

app = FastAPI(title="ModelDock API")

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "ModelDock backend running"}

@app.get("/test-db")
async def test_db():
    collections = await database.list_collection_names()
    return {"collections": collections}