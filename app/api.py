"""FastAPI application setup."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.campaign import router as campaign_router
from api.routes.system import router as system_router
from infrastructure.logging.logger import setup_logging


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(
        title="Codagem — AI Agentic Marketing Engine",
        description="Generate high-quality Instagram campaign packages using autonomous multi-agent workflows.",
        version="1.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(campaign_router)
    app.include_router(system_router)

    return app


app = create_app()
