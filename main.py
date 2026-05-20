"""Main entry point — runs FastAPI with uvicorn."""

import uvicorn
from infrastructure.logging.logger import setup_logging

if __name__ == "__main__":
    setup_logging()
    uvicorn.run(
        "app.api:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
    )
