from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Dict

from backend.app.db.session import get_db
from backend.app.db.models import AppSetting
from backend.app.security.auth import get_current_user

router = APIRouter(dependencies=[Depends(get_current_user)])

class ToggleRequest(BaseModel):
    enabled: bool
    provider: str = "gemini"
    local_ai_url: str = "http://localhost:11434"

@router.get("/", summary="Get all settings")
async def get_settings(db: AsyncSession = Depends(get_db)) -> Dict[str, str]:
    """Retrieve all application settings."""
    result = await db.execute(select(AppSetting))
    settings_db = result.scalars().all()
    
    settings_map = {s.key: s.value for s in settings_db}
    
    # Default to true if not set
    if "ai_enabled" not in settings_map:
        settings_map["ai_enabled"] = "true"
        
    return settings_map

@router.post("/ai", summary="Configure AI settings")
async def configure_ai(request: ToggleRequest, db: AsyncSession = Depends(get_db)):
    """Configure AI provider, kill switch, and local URLs."""
    async def set_setting(key: str, value: str):
        result = await db.execute(select(AppSetting).where(AppSetting.key == key))
        setting = result.scalar_one_or_none()
        if setting:
            setting.value = value
        else:
            db.add(AppSetting(key=key, value=value))

    await set_setting("ai_enabled", "true" if request.enabled else "false")
    await set_setting("ai_provider", request.provider)
    await set_setting("local_ai_url", request.local_ai_url)
        
    await db.commit()
    return {"status": "success", "ai_enabled": request.enabled, "provider": request.provider}
