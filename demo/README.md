# Douyin Fashion AI — Runnable Demo

A self-contained executable demo of the Douyin Fashion AI platform. Includes a FastAPI backend with mock inference routing + a polished web UI. Runs on any fresh Linux system with Docker or Python.

## Quick Start (Docker — Recommended)

```bash
cd demo
cp .env.example .env
docker compose up --build
```

Then open: **http://localhost:8000**

## Quick Start (Python — No Docker)

```bash
cd demo
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

Then open: **http://localhost:8000**

## What the Demo Does

1. **Upload garment image** (front / back / detail shot)
2. **Select a video template** (Runway Walk, Studio Luxury, Street Style, etc.)
3. **Write or auto-enhance a prompt** (Chinese or English)
4. **Choose AI model persona** (East Asian, International, Luxury Editorial, etc.)
5. **Select inference route** (Economy / Standard / Premium)
6. **Submit job** — backend simulates generation with progress polling
7. **Preview result** — shows mock video metadata + download button

## Demo Architecture

```
demo/
├── main.py               # FastAPI app entrypoint
├── routers/
│   ├── jobs.py           # Job submission & polling
│   ├── prompts.py        # Prompt enhancement
│   └── assets.py         # File upload handling
├── services/
│   ├── inference_router.py   # Mock inference routing logic
│   ├── prompt_enhancer.py    # Prompt rewrite service
│   └── job_store.py          # In-memory job state store
├── static/
│   ├── index.html        # Main UI (single-page)
│   ├── style.css         # Tailwind-inspired custom CSS
│   └── app.js            # Frontend logic
├── sample_assets/
│   └── sample_garment.jpg    # Example garment image
├── requirements.txt
├── .env.example
├── Dockerfile
└── docker-compose.yml
```

## Environment Variables

See `.env.example`. For the demo, all AI inference is mocked — no real API keys needed.
To connect real providers, set `KLING_API_KEY`, `VEO_API_KEY`, or `FALLBACK_PROVIDER_API_KEY`.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/jobs` | Submit a generation job |
| GET | `/api/jobs/{job_id}` | Poll job status |
| GET | `/api/jobs` | List all jobs |
| POST | `/api/prompts/enhance` | Enhance a user prompt |
| POST | `/api/assets/upload` | Upload garment image |
| GET | `/api/templates` | List available templates |
| GET | `/health` | Health check |

## Notes

- All inference is **mocked** in the demo (simulated 5–15 second generation time)
- Job state is stored **in-memory** (resets on restart)
- The demo is NOT production-ready — it shows the UX flow and API contract
- To plug in real inference: edit `services/inference_router.py`
