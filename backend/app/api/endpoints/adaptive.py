from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field, validator
from typing import List, Any
from sqlalchemy.future import select
from backend.app.db.models import AdaptiveRule
from backend.app.db.session import AsyncSessionLocal
from backend.app.security.auth import get_current_user
from backend.app.core.logging import AuditLogger
import re

router = APIRouter(dependencies=[Depends(get_current_user)])

class AdaptiveRuleSubmit(BaseModel):
    vendor: str = Field(..., max_length=50)
    raw_pattern: str = Field(..., max_length=500, min_length=1)
    mapped_control: str = Field(..., max_length=100)
    mapped_value: Any
    
    @validator('vendor')
    def vendor_must_be_alphanumeric(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]+$', v) and v != "all":
            raise ValueError('vendor must be alphanumeric or "all"')
        return v
        
    @validator('mapped_control')
    def control_must_be_valid(cls, v):
        if not re.match(r'^[a-zA-Z0-9_\.]+$', v):
            raise ValueError('mapped_control must only contain letters, numbers, underscores, and dots')
        return v

class AdaptiveRuleResponse(BaseModel):
    id: str
    vendor: str
    raw_pattern: str
    mapped_control: str
    mapped_value: Any
    status: str

@router.post("/submit", response_model=AdaptiveRuleResponse, summary="Submit a new adaptive learning rule")
async def submit_rule(rule: AdaptiveRuleSubmit):
    """
    Submits a new rule mapping a raw configuration pattern to a deterministic control value.
    Used to handle UNKNOWN findings.
    """
    async with AsyncSessionLocal() as db:
        new_rule = AdaptiveRule(
            vendor=rule.vendor,
            raw_pattern=rule.raw_pattern,
            mapped_control=rule.mapped_control,
            mapped_value_json=rule.mapped_value,
            status="APPROVED"
        )
        db.add(new_rule)
        await db.commit()
        await db.refresh(new_rule)
        
        AuditLogger.log_event("ADAPTIVE_RULE_SUBMITTED", {"rule_id": new_rule.id, "vendor": new_rule.vendor, "control": new_rule.mapped_control})
        
        return AdaptiveRuleResponse(
            id=new_rule.id,
            vendor=new_rule.vendor,
            raw_pattern=new_rule.raw_pattern,
            mapped_control=new_rule.mapped_control,
            mapped_value=new_rule.mapped_value_json,
            status=new_rule.status
        )

@router.get("/rules", response_model=List[AdaptiveRuleResponse], summary="List all adaptive rules")
async def list_rules():
    """Returns all adaptive rules."""
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(AdaptiveRule))
        rules = result.scalars().all()
        return [
            AdaptiveRuleResponse(
                id=r.id,
                vendor=r.vendor,
                raw_pattern=r.raw_pattern,
                mapped_control=r.mapped_control,
                mapped_value=r.mapped_value_json,
                status=r.status
            ) for r in rules
        ]
