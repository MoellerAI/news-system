import abc
import logging
import os
from datetime import datetime
from enum import StrEnum
from typing import Any, Dict, List, Optional

import openai
from pydantic import BaseModel, Field


class InvestigationTask(BaseModel):
    task_id: str
    description: str
    content: str
    assigned_to: str
    status: str = "pending"  # pending, running, done, failed
    result: Any = None
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None


class LeadType(StrEnum):
    FILE = "file"
    QUESTION = "question"
    EMAIL = "email"


class Lead(BaseModel):
    lead_id: str
    lead_type: LeadType
    content: str
    status: str = Field(default="new")
    timestamp: datetime = Field(default_factory=datetime.now)


class Source(BaseModel):
    source_id: str
    content: str
    origin: Optional[str]
    timestamp: datetime = Field(default_factory=datetime.now)


class Article(BaseModel):
    article_id: str
    title: str
    content: str
    author: str
    timestamp: datetime = Field(default_factory=datetime.now)
