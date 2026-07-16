import asyncio
import random
import logging
import os
from datetime import datetime, timezone

from services.job_store import job_store

logger = logging.getLogger(__name__)

ROUTE_TIMING = {
    "economy": (5, 10),
    "standard": (8, 15),
    "premium": (12, 20),
}

ROUTE_COST = {
    "economy": 1.50,
    "standard": 4.50,
    "premium": 15.00,
}

MOCK_VIDEO_URLS = {
    "runway_walk": "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
    "studio_luxury": "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
    "street_style": "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",
    "detail_closeup": "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4",
    "festive_campaign": "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4",
    "outdoor_cinematic": "https://storage.googleapis.com/gtv-videos-bucket/sample/SubaruOutbackOnStreetAndDirt.mp4",
}


async def run_inference_mock(job_id: str, params: dict):
    """Simulate the full generation pipeline with realistic progress updates."""
    route = params.get("route", "standard")
    template = params.get("template", "studio_luxury")
    min_t, max_t = ROUTE_TIMING.get(route, (8, 15))
    total_time = random.uniform(min_t, max_t)

    steps = [
        (0.05, "preprocessing", "Preprocessing garment images..."),
        (0.20, "preprocessing", "Segmenting garment from background..."),
        (0.35, "tryon", "Binding garment to model persona..."),
        (0.50, "generating", "Sending to inference router..."),
        (0.65, "generating", f"Generating video via {route.capitalize()} route..."),
        (0.80, "generating", "Running quality checks..."),
        (0.90, "postprocessing", "Applying color grading and audio..."),
        (0.95, "postprocessing", "Encoding to 9:16 vertical format..."),
        (1.00, "completed", "Video ready!"),
    ]

    job_store.update(job_id, status="processing", progress=5, message="Job picked up by worker")

    for fraction, stage, message in steps:
        await asyncio.sleep(total_time * (fraction if fraction < 1.0 else 0.05))
        progress = int(fraction * 100)

        if fraction < 1.0:
            job_store.update(job_id, status="processing", progress=progress, message=message)
        else:
            # Simulate occasional failure (5% chance)
            if random.random() < 0.05:
                job_store.update(
                    job_id,
                    status="failed",
                    progress=95,
                    message="Generation failed: model quality threshold not met. Please retry.",
                )
                logger.warning("Job %s failed (simulated)", job_id)
                return

            result = {
                "video_url": MOCK_VIDEO_URLS.get(template, MOCK_VIDEO_URLS["studio_luxury"]),
                "thumbnail_url": f"https://picsum.photos/seed/{job_id[:8]}/540/960",
                "duration_seconds": params.get("duration_seconds", 8),
                "resolution": "1080x1920",
                "aspect_ratio": "9:16",
                "route_used": route,
                "template_used": template,
                "persona_used": params.get("persona", "east_asian"),
                "cost_usd": round(ROUTE_COST.get(route, 4.50) * random.uniform(0.9, 1.1), 2),
                "quality_score": round(random.uniform(0.72, 0.96), 2),
                "garment_fidelity_score": round(random.uniform(0.75, 0.95), 2),
                "generated_at": datetime.now(timezone.utc).isoformat(),
            }
            job_store.update(job_id, status="completed", progress=100, message="Video generated successfully!", result=result)
            logger.info("Job %s completed | quality=%.2f cost=$%.2f", job_id, result["quality_score"], result["cost_usd"])
