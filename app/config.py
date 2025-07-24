import os
from typing import Optional

def _require(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required env variable: {name}")
    return value

SUPABASE_URL: str = _require("SUPABASE_URL")
SUPABASE_PUBLISHABLE_KEY: str = _require("SUPABASE_PUBLISHABLE_KEY")
SUPABASE_SECRET_KEY: Optional[str] = os.getenv("SUPABASE_SECRET_KEY")
