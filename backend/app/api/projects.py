from datetime import datetime

from fastapi import APIRouter

from app.db.database import projects_collection
from app.schemas.project import ProjectCreate, ProjectResponse


router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", response_model=ProjectResponse)
async def create_project(project: ProjectCreate) -> ProjectResponse:
    doc = {
        "name": project.name,
        "created_at": datetime.utcnow(),
    }
    result = await projects_collection.insert_one(doc)

    return ProjectResponse(id=str(result.inserted_id), name=project.name)


@router.get("", response_model=list[ProjectResponse])
async def list_projects() -> list[ProjectResponse]:
    cursor = projects_collection.find()
    projects: list[ProjectResponse] = []

    async for doc in cursor:
        projects.append(
            ProjectResponse(
                id=str(doc["_id"]),
                name=doc.get("name", ""),
            )
        )

    return projects

