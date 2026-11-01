from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field

from app import llm
from app.config import Settings, get_settings

app = FastAPI(title="HintForge", version="0.2.0")

SettingsDep = Annotated[Settings, Depends(get_settings)]


class ChatIn(BaseModel):
    prompt: str = Field(min_length=1, max_length=4000)


@app.get("/health")
def health(settings: SettingsDep) -> dict:
    """Liveness: the process is up. Must be fast and must not call the LLM or the DB."""
    return {"status": "ok", "app": settings.app_name, "environment": settings.environment}


@app.post("/chat")
def chat(body: ChatIn) -> dict:
    """Send a prompt to the LLM (primary model, automatic fallback)."""
    try:
        return llm.chat([{"role": "user", "content": body.prompt}])
    except llm.LLMUnavailable as e:
        raise HTTPException(status_code=503, detail=f"LLM unavailable: {e}") from e


@app.get("/usage")
def usage() -> dict:
    """Total tokens and cost since the app started."""
    return llm.get_usage()
