from __future__ import annotations

"""
Models for the CSV Operations
"""

from pydantic import BaseModel
from typing import Optional


class CSVModel(BaseModel):
    url: str
    topic: str


class CSVModelResponse(CSVModel):
    id: str


class HeaderModel(BaseModel):
    id: Optional[str]
    name: Optional[str]


class HeaderModelResponse(HeaderModel):
    id: str
    header: list[str]


class ErrorResponse(BaseModel):
    status_code: int
    message: str
