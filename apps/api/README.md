# MPH Handwriting API

FastAPI backend for transcribing handwritten construction proposals and generating professional documents.

## Setup

```bash
cd apps/api
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -e .
```

## Run

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Environment Variables

Copy `.env.example` to `.env` and configure:
- `OPENAI_API_KEY`: Your OpenAI API key
