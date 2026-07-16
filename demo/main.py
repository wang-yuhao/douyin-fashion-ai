import os
import logging
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from routers import jobs, prompts, assets, templates

logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "info").upper()),
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Path("uploads").mkdir(exist_ok=True)
    logger.info("Douyin Fashion AI Demo started — http://localhost:%s", os.getenv("APP_PORT", "8000"))
    yield
    logger.info("Shutting down.")


app = FastAPI(
    title="Douyin Fashion AI — Demo",
    description="MVP demo: garment-to-video generation platform for Chinese apparel market",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jobs.router, prefix="/api/jobs", tags=["jobs"])
app.include_router(prompts.router, prefix="/api/prompts", tags=["prompts"])
app.include_router(assets.router, prefix="/api/assets", tags=["assets"])
app.include_router(templates.router, prefix="/api/templates", tags=["templates"])

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "douyin-fashion-ai-demo", "version": "0.1.0"}


@app.get("/", include_in_schema=False)
async def root():
    return FileResponse("static/index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("APP_PORT", "8000")),
        reload=os.getenv("APP_ENV") == "development",
        log_level=os.getenv("LOG_LEVEL", "info"),
    )
