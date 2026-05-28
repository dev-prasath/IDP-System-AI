# =========================================================
# backend/schemas/entity_schema.py
# =========================================================

from pydantic import BaseModel
from typing import Optional


class EntitySchema(BaseModel):

    label: str

    text: str

    confidence: Optional[float] = 0.0

    is_valid: Optional[bool] = True

    validation_message: Optional[str] = "Valid"