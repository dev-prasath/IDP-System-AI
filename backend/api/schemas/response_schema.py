# =========================================================
# backend/schemas/response_schema.py
# FIXED VERSION
# =========================================================

from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from backend.api.schemas.entity_schema import (
    EntitySchema
)

# =========================================================
# RESPONSE SCHEMA
# =========================================================

class ProcessResponseSchema(BaseModel):

    success: bool

    file_name: Optional[str] = ""

    document_type: Optional[str] = ""

    pages: Optional[int] = 1

    ocr_confidence: Optional[float] = 0.0

    ocr_text: Optional[str] = ""

    entities: Optional[
        List[EntitySchema]
    ] = []

    structured_output: Optional[
        Dict[str, Any]
    ] = {}

    boxes: Optional[
        List[Dict[str, Any]]
    ] = []

    table_data: Optional[
        List[Dict[str, Any]]
    ] = []

    message: Optional[str] = ""