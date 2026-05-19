"""LangGraph campaign workflow with reflection/revision loops."""

from __future__ import annotations

import json
import uuid
from typing import Any

from langgraph.graph import StateGraph, END

from app.agents.product_research_agent import ProductResearchAgent
from app.agents.audience_psychology_agent import AudiencePsychologyAgent
from app.agents.strategy_agent import StrategyAgent
from app.agents.instagram_copywriter_agent import InstagramCopywriterAgent
from app.agents.carousel_structure_agent import CarouselStructureAgent
from app.agents.visual_prompt_agent import VisualPromptAgent
from app.agents.hashtag_seo_agent import HashtagSEOAgent
from app.agents.compliance_agent import ComplianceAgent
from app.agents.quality_reviewer_agent import QualityReviewerAgent
from app.tools.image_generation import ImageGenerationTool
from app.memory.memory_manager import MemoryManager
from app.state.campaign_state import CampaignState
from infrastructure.config.settings import get_settings
from infrastructure.logging.logger import get_logger


logger = get_logger("workflow")

# ── Agent instances ─────────────────────────────────
_agents = {
    "product_research": ProductResearchAgent(),
    "audience_psychology": AudiencePsychologyAgent(),
    "strategy": StrategyAgent(),
    "instagram_copywriter": InstagramCopywriterAgent(),
    "carousel_structure": CarouselStructureAgent(),
    "visual_prompt": VisualPromptAgent(),
    "hashtag_seo": HashtagSEOAgent(),
    "compliance": ComplianceAgent(),
    "quality_reviewer": QualityReviewerAgent(),
}

_image_tool = ImageGenerationTool()
_memory = MemoryManager()


# ── Node functions ──────────────────────────────────

async def node_product_research(state: dict) -> dict:
    logger.info("→ ProductResearch node")
    return await _agents["product_research"].run(state)


async def node_audience_psychology(state: dict) -> dict:
    logger.info("→ AudiencePsychology node")
    return await _agents["audience_psychology"].run(state)


async def node_strategy(state: dict) -> dict:
    logger.info("→ Strategy node")
    return await _agents["strategy"].run(state)


async def node_copywriter(state: dict) -> dict:
    logger.info("→ InstagramCopywriter node")
    return await _agents["instagram_copywriter"].run(state)


async def node_carousel(state: dict) -> dict:
    logger.info("→ CarouselStructure node")
    return await _agents["carousel_structure"].run(state)


async def node_visual_prompt(state: dict) -> dict:
    logger.info("→ VisualPrompt node")
    return await _agents["visual_prompt"].run(state)


async def node_image_generation(state: dict) -> dict:
    logger.info("→ ImageGeneration tool node")
    prompt_data = state.get("visual_prompt_data", {})
    prompt = prompt_data.get("cinematic_prompt", "") if isinstance(prompt_data, dict) else ""
    campaign_id = state.get("campaign_id", str(uuid.uuid4()))
    return await _image_tool.generate(prompt, campaign_id=campaign_id)


async def node_hashtag_seo(state: dict) -> dict:
    logger.info("→ HashtagSEO node")
    return await _agents["hashtag_seo"].run(state)


async def node_compliance(state: dict) -> dict:
    logger.info("→ Compliance node")
    return await _agents["compliance"].run(state)


async def node_quality_review(state: dict) -> dict:
    logger.info("→ QualityReview node")
    result = await _agents["quality_reviewer"].run(state)

    # Track revision history
    history = list(state.get("revision_history", []))
    score = result.get("quality_score", 0.0)
    history.append({
        "loop": state.get("review_loop_count", 0) + 1,
        "score": score,
        "target": result.get("revision_target", ""),
    })
    result["revision_history"] = history
    result["review_loop_count"] = state.get("review_loop_count", 0) + 1
    return result


# ── Routing logic ───────────────────────────────────

_REVISION_MAP = {
    "product_data": "product_research",
    "audience_profile": "audience_psychology",
    "strategy": "strategy",
    "copywriting": "instagram_copywriter",
    "carousel_structure": "carousel_structure",
    "visual_prompt_data": "visual_prompt",
    "hashtags": "hashtag_seo",
}


def route_after_review(state: dict) -> str:
    """Decide: revision loop or finalize."""
    settings = get_settings()
    loop_count = state.get("review_loop_count", 0)
    needs_revision = state.get("needs_revision", False)

    if not needs_revision:
        logger.info("Quality threshold PASSED — finalizing")
        return "finalize"

    if loop_count >= settings.max_review_loops:
        logger.warning(f"Max review loops ({settings.max_review_loops}) reached — finalizing with current quality")
        return "finalize"

    target = state.get("revision_target", "")
    next_node = _REVISION_MAP.get(target, "instagram_copywriter")
    logger.info(f"Quality below threshold — revision loop {loop_count}, routing to {next_node}")
    return next_node


async def node_finalize(state: dict) -> dict:
    """Assemble the final campaign output package."""
    logger.info("→ Finalize node — assembling campaign package")

    campaign_id = state.get("campaign_id", str(uuid.uuid4()))
    score = state.get("quality_score", 0.0)
    copy = state.get("copywriting", {})
    hashtags_data = state.get("hashtags", {})
    visual_data = state.get("visual_prompt_data", {})
    audience_data = state.get("audience_profile", {})
    product_data = state.get("product_data", {})
    strategy_data = state.get("strategy", {})
    review_data = state.get("quality_review", {})

    all_hashtags = []
    if isinstance(hashtags_data, dict):
        all_hashtags = (
            hashtags_data.get("primary_hashtags", [])
            + hashtags_data.get("secondary_hashtags", [])
            + hashtags_data.get("niche_hashtags", [])
        )

    final_output = {
        "campaign_id": campaign_id,
        "platform": "instagram",
        "product": {
            "name": state.get("product_name", product_data.get("name", "")),
            "link": state.get("affiliate_link", ""),
            "niche": state.get("niche", ""),
        },
        "content": {
            "headline": copy.get("hooks", [""])[0] if isinstance(copy, dict) else "",
            "caption": copy.get("caption", "") if isinstance(copy, dict) else "",
            "cta": copy.get("cta", "") if isinstance(copy, dict) else "",
            "hashtags": all_hashtags,
            "bio_suggestion": "",
            "carousel_slides": state.get("carousel_structure", []),
            "image_prompt": visual_data.get("cinematic_prompt", "") if isinstance(visual_data, dict) else "",
            "generated_image": state.get("generated_image_path", ""),
        },
        "metadata": {
            "tone": state.get("tone", ""),
            "strategy": strategy_data.get("campaign_strategy", "") if isinstance(strategy_data, dict) else "",
            "persona": audience_data.get("persona", "") if isinstance(audience_data, dict) else "",
            "pain_points": audience_data.get("pain_points", []) if isinstance(audience_data, dict) else [],
            "benefits": product_data.get("benefits", []) if isinstance(product_data, dict) else [],
        },
        "quality": {
            "score": score,
            "review_notes": review_data.get("review_notes", []) if isinstance(review_data, dict) else [],
        },
    }

    # Save to memory
    if score >= get_settings().quality_threshold:
        _memory.save_successful_pattern(campaign_id, "quality_pass", json.dumps(final_output, indent=2))
    else:
        _memory.save_failure(campaign_id, "low_quality", f"Score: {score}")

    review_notes = review_data.get("review_notes", []) if isinstance(review_data, dict) else []
    _memory.save_review(campaign_id, score, review_notes)

    if isinstance(copy, dict) and copy.get("hooks"):
        _memory.save_hook(campaign_id, copy["hooks"])

    _memory.save_niche_knowledge(state.get("niche", ""), json.dumps(product_data, ensure_ascii=False))

    # Save campaign JSON to outputs
    from pathlib import Path
    out_dir = Path("outputs/campaigns")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{campaign_id}.json"
    out_path.write_text(json.dumps(final_output, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info(f"Campaign saved to {out_path}")

    return {
        "final_output": final_output,
        "campaign_id": campaign_id,
        "quality_score": score,
        "current_agent": "finalize",
    }


# ── Build the graph ─────────────────────────────────

def build_campaign_graph() -> StateGraph:
    graph = StateGraph(CampaignState)

    # Add nodes
    graph.add_node("product_research", node_product_research)
    graph.add_node("audience_psychology", node_audience_psychology)
    graph.add_node("strategy", node_strategy)
    graph.add_node("instagram_copywriter", node_copywriter)
    graph.add_node("carousel_structure", node_carousel)
    graph.add_node("visual_prompt", node_visual_prompt)
    graph.add_node("image_generation", node_image_generation)
    graph.add_node("hashtag_seo", node_hashtag_seo)
    graph.add_node("compliance", node_compliance)
    graph.add_node("quality_reviewer", node_quality_review)
    graph.add_node("finalize", node_finalize)

    # Linear sequence
    graph.set_entry_point("product_research")
    graph.add_edge("product_research", "audience_psychology")
    graph.add_edge("audience_psychology", "strategy")
    graph.add_edge("strategy", "instagram_copywriter")
    graph.add_edge("instagram_copywriter", "carousel_structure")
    graph.add_edge("carousel_structure", "visual_prompt")
    graph.add_edge("visual_prompt", "image_generation")
    graph.add_edge("image_generation", "hashtag_seo")
    graph.add_edge("hashtag_seo", "compliance")
    graph.add_edge("compliance", "quality_reviewer")

    # After quality review: either finalize or loop back
    graph.add_conditional_edges(
        "quality_reviewer",
        route_after_review,
        {
            "finalize": "finalize",
            "product_research": "product_research",
            "audience_psychology": "audience_psychology",
            "strategy": "strategy",
            "instagram_copywriter": "instagram_copywriter",
            "carousel_structure": "carousel_structure",
            "visual_prompt": "visual_prompt",
            "hashtag_seo": "hashtag_seo",
        },
    )

    graph.add_edge("finalize", END)

    return graph


def compile_campaign_graph():
    """Build and compile the LangGraph workflow."""
    graph = build_campaign_graph()
    return graph.compile()
