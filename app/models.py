# app/models.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table, Enum, Index
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime
import enum

Base = declarative_base()

# Enum Classes
class ArtType(enum.Enum):
    original = "original"
    ai = "ai"

class AudioType(enum.Enum):
    mix = "mix"
    playlist = "playlist"

# Many-to-Many relation table between Artwork and Audio
art_audio_link = Table('art_audio_link', Base.metadata,
    Column('art_id', Integer, ForeignKey('art.id')),
    Column('audio_id', Integer, ForeignKey('audio.id'))
)

class Art(Base):
    __tablename__ = 'art'

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)  
    description = Column(String, nullable=True)
    type = Column(Enum(ArtType), index=True)
    url = Column(String, nullable=True) 
    colours = Column(ARRAY(String), nullable=True)  
    parent_id = Column(Integer, ForeignKey('art.id')) 
    tags = Column(ARRAY(String), nullable=True) 
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)

    related_artwork = relationship("Art", backref="parent_artwork", remote_side=[id])
    linked_audio = relationship("Audio", secondary=art_audio_link, back_populates="linked_art")

    __table_args__ = (
        Index('idx_art_type_date', 'type', 'created'),
        Index('idx__color_gin', 'colours', postgresql_using='gin'),
        Index('idx_tags_gin', 'tags', postgresql_using='gin')
    )

class Audio(Base):
    __tablename__ = 'audio'

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)  
    type = Column(Enum(AudioType), index=True)
    description = Column(String, nullable=True)
    url = Column(String, nullable=True) 
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)

    linked_art = relationship("Art", secondary=art_audio_link, back_populates="linked_audio")

    __table_args__ = (
        Index('idx_audio_type_date', 'type', 'created'),
    )
