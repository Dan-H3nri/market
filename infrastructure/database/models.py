"""SQLAlchemy ORM models and session management."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Float, Text, DateTime, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from infrastructure.config.settings import get_settings


class Base(DeclarativeBase):
    pass


class CampaignRecord(Base):
    __tablename__ = "campaigns"

    campaign_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    product_name = Column(String, nullable=False)
    affiliate_link = Column(String, nullable=False)
    niche = Column(String, nullable=False)
    audience = Column(String, nullable=False)
    objective = Column(String, default="conversions")
    tone = Column(String, default="persuasive")
    status = Column(String, default="pending")
    quality_score = Column(Float, default=0.0)
    output_json = Column(Text, default="{}")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


_engine = None
_SessionLocal = None


def init_db() -> None:
    global _engine, _SessionLocal
    settings = get_settings()
    _engine = create_engine(settings.database_url, echo=False)
    Base.metadata.create_all(_engine)
    _SessionLocal = sessionmaker(bind=_engine, expire_on_commit=False)


def get_session():
    if _SessionLocal is None:
        init_db()
    return _SessionLocal()
