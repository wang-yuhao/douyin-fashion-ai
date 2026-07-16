from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class Template(BaseModel):
    id: str
    name_en: str
    name_zh: str
    description: str
    recommended_route: str
    duration_seconds: int
    tags: list[str]


TEMPLATES = [
    Template(
        id="runway_walk",
        name_en="Runway Walk",
        name_zh="T台走秀",
        description="Model walks a high-fashion runway under dramatic studio lighting",
        recommended_route="premium",
        duration_seconds=10,
        tags=["luxury", "editorial", "high-fashion"],
    ),
    Template(
        id="studio_luxury",
        name_en="Studio Luxury",
        name_zh="奢华棚拍",
        description="Clean white studio with cinematic lighting, full outfit showcase",
        recommended_route="standard",
        duration_seconds=8,
        tags=["studio", "clean", "commercial"],
    ),
    Template(
        id="street_style",
        name_en="Street Style",
        name_zh="街头风格",
        description="Urban street environment, natural movement, lifestyle feel",
        recommended_route="standard",
        duration_seconds=8,
        tags=["street", "casual", "lifestyle"],
    ),
    Template(
        id="detail_closeup",
        name_en="Detail Close-up",
        name_zh="细节特写",
        description="Macro shots highlighting fabric texture, stitching, and material quality",
        recommended_route="economy",
        duration_seconds=6,
        tags=["detail", "fabric", "quality"],
    ),
    Template(
        id="festive_campaign",
        name_en="Festive Campaign",
        name_zh="节庆营销",
        description="Vibrant festive backdrop, celebratory mood for seasonal campaigns",
        recommended_route="standard",
        duration_seconds=10,
        tags=["festive", "campaign", "seasonal"],
    ),
    Template(
        id="outdoor_cinematic",
        name_en="Outdoor Cinematic",
        name_zh="户外电影感",
        description="Golden hour outdoor with cinematic color grading and natural movement",
        recommended_route="premium",
        duration_seconds=12,
        tags=["outdoor", "cinematic", "nature"],
    ),
]


@router.get("", response_model=list[Template])
async def list_templates():
    return TEMPLATES


@router.get("/{template_id}", response_model=Template)
async def get_template(template_id: str):
    for t in TEMPLATES:
        if t.id == template_id:
            return t
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Template not found")
