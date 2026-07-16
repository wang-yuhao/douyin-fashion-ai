import threading
from datetime import datetime, timezone
from typing import Optional


class JobStore:
    """Thread-safe in-memory job store for demo purposes."""

    def __init__(self):
        self._store: dict[str, dict] = {}
        self._lock = threading.Lock()

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def create(self, job_id: str, params: dict) -> dict:
        job = {
            "job_id": job_id,
            "status": "queued",
            "progress": 0,
            "message": "Job queued — waiting for worker",
            "result": None,
            "params": params,
            "created_at": self._now(),
            "updated_at": self._now(),
        }
        with self._lock:
            self._store[job_id] = job
        return job

    def update(self, job_id: str, **kwargs) -> Optional[dict]:
        with self._lock:
            if job_id not in self._store:
                return None
            self._store[job_id].update(kwargs)
            self._store[job_id]["updated_at"] = self._now()
            return self._store[job_id].copy()

    def get(self, job_id: str) -> Optional[dict]:
        with self._lock:
            return self._store.get(job_id)

    def list_all(self) -> list[dict]:
        with self._lock:
            return list(self._store.values())

    def delete(self, job_id: str) -> bool:
        with self._lock:
            if job_id not in self._store:
                return False
            del self._store[job_id]
            return True


job_store = JobStore()
