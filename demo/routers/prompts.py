import logging
from fastapi import APIRouter
from pydantic import BaseModel

from services.prompt_enhancer import enhance_prompt

logger = logging.getLogger(__name__)
router = APIRouter()


class PromptRequest(BaseModel):
    prompt: str
    template: str = "studio_luxury"
    persona: str = "east_asian"
    language: str = "zh-CN"


class PromptResponse(BaseModel):
    original: str
    enhanced: str
    tokens_used: int
    language_detected: str


@router.post("/enhance", response_model=PromptResponse)
async def enhance(req: PromptRequest):
    result = enhance_prompt(req.prompt, req.template, req.persona, req.language)
    logger.info("Prompt enhanced | template=%s lang=%s", req.template, req.language)
    return result
