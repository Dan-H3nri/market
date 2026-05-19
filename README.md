# Codagem — AI Agentic Marketing Engine

An AI-powered marketing operating system that generates high-quality Instagram campaign packages using autonomous multi-agent workflows orchestrated with LangGraph.

## Architecture

```
INPUT → ProductResearch → AudiencePsychology → Strategy → Copywriter → Carousel → VisualPrompt → ImageGeneration → HashtagSEO → Compliance → QualityReview → OUTPUT
                                                                                                                                                    ↑_________|
                                                                                                                                                (reflection loop)
```

### Agent Pipeline

| Agent | Role |
|---|---|
| ProductResearch | Analyze products, benefits, differentiators, positioning |
| AudiencePsychology | Personas, emotional triggers, pain points, objections |
| Strategy | Campaign strategy, persuasion structure, storytelling |
| InstagramCopywriter | Hooks, captions, CTA, engagement optimization |
| CarouselStructure | Slide-by-slide narrative, retention optimization |
| VisualPrompt | Cinematic image prompts, visual direction |
| ImageGeneration (tool) | Generate campaign images via API |
| HashtagSEO | Hashtags, keyword strategy, discoverability |
| Compliance | Spam detection, claim review, policy compliance |
| QualityReviewer | Score quality, identify weak sections, trigger revisions |

### Reflection Loops

If the quality score is below `QUALITY_THRESHOLD`, the system automatically routes back to the weak agent for revision. Maximum loops controlled by `MAX_REVIEW_LOOPS`.

## Quick Start

### 1. Setup

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 2. Install

```bash
pip install -r requirements.txt
```

### 3. Run API

```bash
python main.py
# API at http://localhost:8000
```

### 4. Run Frontend

```bash
streamlit run frontend/app.py
# UI at http://localhost:8501
```

### 5. Docker

```bash
docker compose up
```

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `PRIMARY_MODEL` | Primary LLM model | `gpt-4o` |
| `PRIMARY_MODEL_URL` | Primary API endpoint | `https://api.openai.com/v1` |
| `PRIMARY_API_KEY` | Primary API key | — |
| `SECONDARY_MODEL` | Fallback LLM | `gpt-4o-mini` |
| `IMAGE_PROVIDER` | Image provider name | `catgpt` |
| `IMAGE_API_URL` | Image API endpoint | `http://localhost:8000/v1` |
| `MAX_REVIEW_LOOPS` | Max revision iterations | `5` |
| `QUALITY_THRESHOLD` | Min score to pass (0-10) | `8.5` |

See `.env.example` for the full list.

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/v1/generate-campaign` | Generate a full campaign package |
| `GET` | `/api/v1/campaigns/{id}` | Retrieve a stored campaign |
| `GET` | `/health` | Health check |
| `GET` | `/agents` | List all agents |
| `GET` | `/workflows` | List workflows |

### Example Request

```bash
curl -X POST http://localhost:8000/api/v1/generate-campaign \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Premium Wireless Earbuds",
    "affiliate_link": "https://example.com/earbuds",
    "niche": "Tech",
    "audience": "Young professionals 25-35",
    "objective": "conversions",
    "tone": "persuasive"
  }'
```

### Example Output

```json
{
  "campaign_id": "uuid",
  "platform": "instagram",
  "product": { "name": "...", "link": "...", "niche": "..." },
  "content": {
    "headline": "...",
    "caption": "...",
    "cta": "...",
    "hashtags": ["..."],
    "carousel_slides": [...],
    "image_prompt": "...",
    "generated_image": "outputs/images/uuid.png"
  },
  "metadata": {
    "tone": "persuasive",
    "strategy": "...",
    "persona": "...",
    "pain_points": ["..."],
    "benefits": ["..."]
  },
  "quality": {
    "score": 9.0,
    "review_notes": ["..."]
  }
}
```

## Project Structure

```
app/
  core/            # Core shared utilities
  graph/           # LangGraph workflow definitions
  agents/          # Specialized agent implementations
  workflows/       # Higher-level workflow compositions
  memory/          # Memory manager (Obsidian-compatible markdown)
  state/           # Typed state definitions
  prompts/         # Prompt templates
  tools/           # Tools (image generation, etc.)
  models/          # Pydantic schemas
  validators/      # Input validation
  utils/           # Utility functions
  api.py           # FastAPI app factory

api/
  routes/          # API endpoint handlers
  middleware/      # Middleware

infrastructure/
  database/        # SQLAlchemy models & sessions
  config/          # Settings & env configuration
  providers/       # LLM provider abstraction
  logging/         # Structured logging
  services/        # Business services

frontend/          # Streamlit UI
memory/            # Persistent markdown memory (Obsidian-compatible)
outputs/           # Generated campaigns, images, logs
tests/             # Test suite
```

## License

MIT
