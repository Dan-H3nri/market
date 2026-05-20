"""Campaign service — orchestrates workflow execution and persistence."""

from __future__ import annotations

import json
import uuid

from app.graph.campaign_workflow import compile_campaign_graph
from app.validators.campaign_validator import validate_campaign_request
from infrastructure.database.models import CampaignRecord, get_session, init_db
from infrastructure.logging.logger import get_logger

logger = get_logger("campaign_service")

_graph = None


def _get_graph():
    global _graph
    if _graph is None:
        _graph = compile_campaign_graph()
    return _graph


async def run_campaign(data: dict) -> dict:
    """Validate input, execute workflow, persist results."""
    init_db()

    request = validate_campaign_request(data)
    logger.info(f"Campaign requested: {request.product_name} in {request.niche}")

    campaign_id = str(uuid.uuid4())

    initial_state = {
        "product_name": request.product_name,
        "affiliate_link": request.affiliate_link,
        "niche": request.niche,
        "audience": request.audience,
        "objective": request.objective,
        "tone": request.tone,
        "campaign_id": campaign_id,
        "revision_history": [],
        "review_loop_count": 0,
        "quality_score": 0.0,
        "needs_revision": False,
    }

    graph = _get_graph()
    final_state = await graph.ainvoke(initial_state, config={"recursion_limit": 100})

    # Persist to DB
    session = get_session()
    try:
        record = CampaignRecord(
            campaign_id=campaign_id,
            product_name=request.product_name,
            affiliate_link=request.affiliate_link,
            niche=request.niche,
            audience=request.audience,
            objective=request.objective,
            tone=request.tone,
            status="completed",
            quality_score=final_state.get("quality_score", 0.0),
            output_json=json.dumps(final_state.get("final_output", {}), ensure_ascii=False),
        )
        session.add(record)
        session.commit()
        logger.info(f"Campaign {campaign_id} persisted to DB")
    except Exception as exc:
        session.rollback()
        logger.error(f"DB persistence failed: {exc}")
    finally:
        session.close()

    return final_state.get("final_output", {})


async def get_campaign(campaign_id: str) -> dict | None:
    init_db()
    session = get_session()
    try:
        record = session.query(CampaignRecord).filter_by(campaign_id=campaign_id).first()
        if record:
            return json.loads(record.output_json)
        return None
    finally:
        session.close()
