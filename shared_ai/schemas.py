from pydantic import BaseModel, Field
from typing import Literal

class SupportDraft(BaseModel):
    category: Literal["refund", "login", "delivery", "billing", "technical", "other"]
    draft_reply: str = Field(min_length=1, max_length=4000)
    needs_human_review: bool = True

class ActionItem(BaseModel):
    task: str = Field(min_length=1, max_length=500)
    owner: str | None = None
    due_date: str | None = None

class ResearchClaim(BaseModel):
    claim: str
    evidence: list[str] = []
    status: Literal["supported", "contradicted", "unverified"] = "unverified"
