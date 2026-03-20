# 🎯 AI Job Notifier

An AI-powered job matching platform with resume parsing, semantic search, and personalized recommendations.

## Architecture

```
AI_JOB_Notifier/
├── backend/              # FastAPI (Python)
│   ├── core/             # Config, DB, security, middleware
│   ├── models/           # SQLAlchemy models (User, Job)
│   ├── schemas/          # Pydantic schemas
│   ├── routes/           # API endpoints
│   ├── services/         # Business logic
│   ├── nlp/              # Resume parser (PDF/DOCX → skills/experience/education)
│   ├── vectorstore/      # Sentence-transformers + FAISS
│   ├── matching/         # Job matching engine (weighted scoring)
│   ├── rag/              # RAG pipeline (LangChain + OpenAI)
│   ├── scraper/          # Job scraper (BeautifulSoup)
│   └── notifications/    # Async email alerts (SMTP)
├── frontend/             # Next.js + Tailwind CSS
│   ├── src/app/          # Pages (Dashboard, Upload, Jobs, Profile)
│   ├── src/components/   # UI components
│   └── src/lib/          # API client
└── README.md
```

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL

### Backend Setup

```bash
cd backend
cp .env.example .env      # Edit with your credentials
pip install -r requirements.txt
python -m spacy download en_core_web_sm
uvicorn backend.main:app --reload
```

API Docs: http://localhost:8000/docs

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

UI: http://localhost:3000

## Key Features

| Feature | Tech |
|---------|------|
| JWT Auth | python-jose + bcrypt |
| Resume Parser | pdfplumber + python-docx + regex NLP |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Vector Search | FAISS |
| Job Matching | 0.5×similarity + 0.3×skill + 0.2×experience |
| RAG (AI Q&A) | LangChain + OpenAI |
| Job Scraping | BeautifulSoup + retry |
| Notifications | aiosmtplib (async) |
| Frontend | Next.js + TypeScript + Tailwind CSS |

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /api/v1/auth/register | Register |
| POST | /api/v1/auth/login | Login (JWT) |
| POST | /api/v1/resume/upload | Upload resume (PDF/DOCX) |
| GET | /api/v1/jobs | List jobs (filterable) |
| GET | /api/v1/jobs/{id} | Job detail |
| GET | /api/v1/recommendations | Personalized matches |
| POST | /api/v1/recommendations/ask | RAG Q&A |

## Environment Variables

See `.env.example` for full list. Key ones:
- `DATABASE_URL` — PostgreSQL connection string
- `JWT_SECRET_KEY` — Change in production!
- `OPENAI_API_KEY` — For RAG pipeline
- `SMTP_*` — For email notifications
