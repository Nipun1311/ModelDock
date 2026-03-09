from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import database
from app.api.auth import router as auth_router
from app.api.projects import router as project_router
from app.api.datasets import router as dataset_router

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

app.include_router(auth_router)
app.include_router(project_router)
app.include_router(dataset_router)


@app.get("/")
async def root():
    return {"message": "ModelDock backend running"}


@app.get("/test-db")
async def test_db():
    collections = await database.list_collection_names()
    return {"collections": collections}