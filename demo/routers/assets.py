import uuid
import shutil
import logging
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)
router = APIRouter()

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_SIZE_MB = 20
UPLOAD_DIR = Path("uploads")


class AssetResponse(BaseModel):
    asset_id: str
    filename: str
    content_type: str
    size_bytes: int
    url: str


@router.post("/upload", response_model=AssetResponse)
async def upload_asset(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}. Use JPEG, PNG, or WebP.")

    content = await file.read()
    if len(content) > MAX_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=413, detail=f"File exceeds {MAX_SIZE_MB}MB limit")

    asset_id = str(uuid.uuid4())
    ext = Path(file.filename).suffix or ".jpg"
    save_path = UPLOAD_DIR / f"{asset_id}{ext}"
    UPLOAD_DIR.mkdir(exist_ok=True)

    with open(save_path, "wb") as f:
        f.write(content)

    logger.info("Asset uploaded: %s (%d bytes)", asset_id, len(content))
    return AssetResponse(
        asset_id=asset_id,
        filename=file.filename,
        content_type=file.content_type,
        size_bytes=len(content),
        url=f"/uploads/{asset_id}{ext}",
    )
