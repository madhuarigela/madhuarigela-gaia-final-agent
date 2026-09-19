import os
from pathlib import Path
import requests

BASE = os.getenv("GAIA_API_BASE_URL", "https://agents-course-unit4-scoring.hf.space")
DOWNLOAD_DIR = Path(os.getenv("GAIA_DOWNLOAD_DIR", "./downloads"))

def get_questions():
    r = requests.get(f"{BASE}/questions", timeout=30)
    r.raise_for_status()
    data = r.json()
    return data.get("questions", data) if isinstance(data, dict) else data

def download_attachment(task_id, filename=None):
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    r = requests.get(f"{BASE}/files/{task_id}", timeout=30)
    if r.status_code == 404:
        return None
    r.raise_for_status()
    path = DOWNLOAD_DIR / (Path(filename).name if filename else f"{task_id}.bin")
    path.write_bytes(r.content)
    return path

def submit(username, space_id, answers):
    payload = {
        "username": username,
        "agent_code": f"https://huggingface.co/spaces/{space_id}/tree/main",
        "answers": answers,
    }
    r = requests.post(f"{BASE}/submit", json=payload, timeout=120)
    r.raise_for_status()
    return r.json()
