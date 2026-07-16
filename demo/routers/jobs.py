import uuid
import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field

from services.job_store import job_store
from services.inference_router import run_inference_mock

logger = logging.getLogger(__name__)
router = APIRouter()


class JobRequest(BaseModel):
    asset_id: str = Field(..., description="ID of the uploaded garment asset")
    template: str = Field(..., description="Template name (e.g. runway_walk)")
    prompt: str = Field("", description="User prompt (Chinese or English)")
    enhanced_prompt: str = Field("", description="Enhanced prompt from prompt service")
    persona: str = Field("east_asian", description="AI model persona")
    route: str = Field("standard", description="Inference route: economy | standard | premium")
    duration_seconds: int = Field(8, ge=4, le=30)
    aspect_ratio: str = Field("9:16")


class JobResponse(BaseModel):
    job_id: str
    status: str
    progress: int
    message: str
    result: Optional[dict] = None
    created_at: str
    updated_at: str


@router.post("", response_model=JobResponse, status_code=202)
async def submit_job(req: JobRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    job = job_store.create(job_id, req.model_dump())
    background_tasks.add_task(run_inference_mock, job_id, req.model_dump())
    logger.info("Job %s submitted | route=%s template=%s", job_id, req.route, req.template)
    return job


@router.get("", response_model=list[JobResponse])
async def list_jobs():
    return job_store.list_all()


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: str):
    job = job_store.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.delete("/{job_id}", status_code=204)
async def delete_job(job_id: str):
    if not job_store.delete(job_id):
        raise HTTPException(status_code=404, detail="Job not found")
