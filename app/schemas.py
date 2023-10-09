# app/schemas.py

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import enum

# Enum Classes for Pydantic models
class ArtType(str, enum.Enum):
    original = "original"
    ai = "ai"

class AudioType(str, enum.Enum):
    mix = "mix"
    playlist = "playlist"

# Pydantic models for Art
class ArtBase(BaseModel):
    title: str
    description: Optional[str] = None
    type: ArtType
    colours: Optional[List[str]] = None
    tags: Optional[List[str]] = None

class ArtCreate(ArtBase):
    parent_id: Optional[int] = None
    image: bytes  # Accepts binary image data

class ArtUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[ArtType] = None
    url: Optional[str] = None
    colours: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    parent_id: Optional[int] = None 

class ArtRead(ArtBase):
    id: int
    parent_id: Optional[int] = None
    url: Optional[str]  # Adding URL field
    created: datetime
    updated: datetime

    class Config:
        from_attributes = True

class ArtReadDetail(ArtRead):
    related_artwork: Optional[List[ArtRead]] = None

# Pydantic models for Audio
class AudioBase(BaseModel):
    title: str
    type: AudioType
    description: Optional[str] = None

class AudioCreate(AudioBase):
    pass

class AudioUpdate(AudioBase):
    id: int

class AudioRead(AudioBase):
    id: int
    created: datetime
    updated: Optional[datetime] = None

    class Config:
        from_attributes = True
