import json
import time
from pathlib import Path


CACHE_DIR = Path.home() / ".cache" / "shellsense"
CACHE_TTL = 60 * 60 * 24 * 30   # 30 days in seconds


def _cache_path(command: str) -> Path:
    safe_name = command.replace("/", "_").replace(" ", "_")
    return CACHE_DIR / f"{safe_name}.json"


def get(command: str) -> dict | None:
    path = _cache_path(command)

    if not path.exists():
        return None

    try:
        data = json.loads(path.read_text())

        # Check if the cache entry has expired
        cached_time = data.get("_cached_at", 0)
        if time.time() - cached_time > CACHE_TTL:
            path.unlink()  # Delete expired entry
            return None

        return data

    except (json.JSONDecodeError, KeyError):
        return None


def put(command: str, data: dict) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    data["_cached_at"] = time.time()
    path = _cache_path(command)
    path.write_text(json.dumps(data, indent=2))


def clear() -> int:
    if not CACHE_DIR.exists():
        return 0

    count = 0
    for file in CACHE_DIR.glob("*.json"):
        file.unlink()
        count += 1

    return count