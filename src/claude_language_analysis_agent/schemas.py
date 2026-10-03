from typing import Literal

from pydantic import BaseModel, Field

RegisterLabel = Literal["informal", "neutral-professional", "formal-professional", "institutional", "unclear"]

class LanguageAnalysis(BaseModel):
    register_label: RegisterLabel
    directness: int = Field(ge=1, le=5)
    politeness: int = Field(ge=1, le=5)
    ambiguity: int = Field(ge=1, le=5)
    evidence: list[str] = Field(min_length=1)
    revision: str | None = None
