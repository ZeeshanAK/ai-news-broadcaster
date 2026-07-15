# AI News Broadcaster — Development Plan

## Project Overview

The **AI News Broadcaster** is a comprehensive, end-to-end news aggregation and broadcasting system. It automatically fetches news from multiple sources, intelligently filters and summarizes them using LLMs, converts summaries to audio, and delivers broadcasts to users via Telegram and other channels.

### Core Value Proposition
- **Automated pipeline**: Fetch → Filter → Summarize → Audio → Deliver
- **Intelligent curation**: Only broadcast news that matters using LLM-driven relevance classification
- **Multi-channel delivery**: Start with Telegram, extend to email, RSS, podcasts
- **Customizable**: Users can configure sources, summaries styles, delivery preferences

---

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                     Frontend (React + Vite)                     │
│  Dashboard | Settings | Analytics | Source Management          │
└─────────────────────────────────────────────────────────────────┘
                              ↕ HTTP/REST
┌─────────────────────────────────────────────────────────────────┐
│                    Backend API (FastAPI)                        │
│  /api/v1/articles | /sources | /summaries | /broadcasts         │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                  Services (Business Logic)                      │
│  ┌──────────┐  ┌────────────┐  ┌────────┐  ┌──────────┐        │
│  │ Ingestion│  │  Pipeline  │  │ Audio  │  │ Delivery │        │
│  │ RSS/APIs │  │  LLM Proc  │  │  TTS   │  │ Telegram │        │
│  └──────────┘  └────────────┘  └────────┘  └──────────┘        │
│       ↓              ↓              ↓             ↓             │
│  Feed parse    Summarize/Filter  EdgeTTS/EL   Telegram API     │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                  Database (SQLAlchemy)                          │
│  Sources | Articles | Summaries | Broadcasts | Logs             │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Ingestion**: `rss_fetcher` + `api_fetcher` → raw articles → DB
2. **Deduplication**: Remove duplicate URLs and near-duplicates
3. **Filtering**: LLM classifies relevance → keep only valuable news
4. **Summarization**: LLM generates radio-anchor-style summary
5. **TTS**: Convert summary text to audio file
6. **Delivery**: Send audio + text to Telegram, log delivery status

### Scheduling

- **Fetch**: Every 30 minutes (configurable)
- **Summarization**: Every 60 minutes on new articles (configurable)
- **Broadcasting**: Daily at 8 AM (configurable)
- **Manual trigger**: `/api/v1/pipeline/run` endpoint for testing

---

## Development Phases

### Phase 1: Foundation ✅ (Current)
- [x] Project structure and scaffolding
- [x] Database models (SQLAlchemy)
- [x] FastAPI backend with CRUD endpoints
- [x] React frontend skeleton with Tailwind
- [x] API client integration
- [x] Environment configuration

### Phase 2: Ingestion & Processing (In Progress)
- [ ] Implement RSS feed fetching with feedparser
- [ ] Implement news API fetching (NewsAPI.org, Hacker News API)
- [ ] Deduplication logic (URL + embedding-based)
- [ ] Write first Alembic migration
- [ ] Seed test data (3-5 RSS feeds)

### Phase 3: LLM Pipeline
- [ ] Implement LLM client with multi-provider support (OpenAI, Groq, Gemini)
- [ ] Relevance classification prompt (benchmark vs. not relevant)
- [ ] Radio-anchor-style summarization prompt
- [ ] Error handling + fallback providers
- [ ] Test on real articles

### Phase 4: Audio & Delivery
- [ ] EdgeTTS integration (primary, free)
- [ ] ElevenLabs integration (backup, higher quality)
- [ ] Telegram bot setup and testing
- [ ] Audio file storage strategy

### Phase 5: Scheduling & Automation
- [ ] APScheduler configuration
- [ ] Background job orchestration
- [ ] Manual trigger endpoint
- [ ] GitHub Actions cron workflow for deployed version

### Phase 6: Frontend & Monitoring
- [ ] Article listing and filtering UI
- [ ] Source management dashboard
- [ ] Broadcast history and analytics
- [ ] Settings and configuration UI
- [ ] Real-time logs and error tracking

### Phase 7: Quality & Deployment
- [ ] Unit + integration tests
- [ ] Docker containerization
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Production database (PostgreSQL)
- [ ] Documentation and deployment guide

---

## Technology Decisions

### Backend
- **FastAPI**: Modern, async-first, automatic docs
- **SQLAlchemy**: Battle-tested ORM with Alembic for migrations
- **Pydantic**: Type-safe data validation
- **APScheduler**: Lightweight, no additional infrastructure needed for dev

### Frontend
- **React**: Industry standard with great tooling
- **Vite**: Fast build tool, excellent dev experience
- **Tailwind**: Utility-first CSS, quick prototyping
- **Axios**: Simple HTTP client

### External Services
- **OpenAI API**: GPT-4o-mini for summarization (cost-effective)
- **Groq API**: Faster, cheaper LLaMA for fallback
- **EdgeTTS**: Free, no API key required (primary for audio)
- **ElevenLabs**: Higher quality fallback (paid)
- **Telegram Bot API**: Direct, no SDK required

---

## Key Features & Implementation Notes

### 1. Multi-Source Ingestion
- **RSS Feeds**: Most important, used by many news sites
- **News APIs**: Structured data (NewsAPI, HackerNews, arXiv)
- **Web Scrapers**: Fallback for custom sources

### 2. Intelligent Filtering
LLM-driven classification:
```
Prompt: Classify this article as one of:
- BENCHMARK (performance/speed comparison)
- PRODUCT_LAUNCH (new tool/model release)
- LOW_SPEC_MODEL (efficient/edge ML)
- FREE_TOOL (open source / no cost)
- NOT_RELEVANT

Article: [article text]
```

### 3. Summary Style Options
- **Brief**: 1-2 sentences
- **Detailed**: 3-4 paragraphs
- **Bullet points**: Key facts
- **News Anchor**: Conversational, suitable for audio (radio style)

### 4. Delivery Channels
- **Telegram**: Primary for MVP
- **Email**: Future (Gmail/SendGrid)
- **RSS Feed**: Generated feed for subscribers
- **Podcast**: Aggregate audio broadcasts into feed

### 5. Error Handling & Resilience
- LLM provider fallback (OpenAI → Groq → Gemini)
- TTS fallback (EdgeTTS → ElevenLabs)
- Automatic retry on network errors
- Logging all failures for debugging

---

## Database Schema (High Level)

```sql
-- Core tables
sources (id, name, url, type, is_active, last_fetched_at)
articles (id, source_id, title, url, content, summary, status)
summaries (id, article_id, content, style, model_used)
broadcasts (id, article_id, summary_id, title, script, audio_url, status)

-- Support tables
story_clusters (id, name, article_ids) -- Group related articles
deliveries (id, broadcast_id, channel, recipient, status)
user_settings (id, key, value, category)
```

---

## Performance Considerations

1. **Database**: Index on `articles.url`, `articles.status`, `sources.is_active`
2. **API Rate Limiting**: Implement per-IP rate limits on backend
3. **Caching**: Cache LLM responses for duplicate articles
4. **Async Operations**: Use FastAPI async for I/O-heavy operations
5. **Audio Storage**: Store locally in dev, S3 in prod

---

## Monitoring & Observability

1. **Logs**: Structured logging with timestamps and severity
2. **Delivery Logs**: Track which broadcasts went to which channels
3. **Error Tracking**: Log LLM failures, TTS errors, delivery failures
4. **Metrics**: Article ingestion count, summarization success rate, broadcast delivery rate

---

## Future Enhancements

1. **User Preferences**: Allow users to customize category filters, delivery times
2. **Multi-language**: Support articles in different languages
3. **Image/Video**: Include images/videos in broadcasts
4. **Podcast Generation**: Bundle broadcasts into podcast feed
5. **Analytics**: Dashboard showing trending topics, source performance
6. **Collaborative Filtering**: Recommend sources based on user preferences
7. **Mobile App**: Native app for iOS/Android
8. **Custom Providers**: Allow users to add their own news sources

---

## Getting Started Checklist

- [x] Set up project structure
- [x] Create database models
- [x] Create API endpoints (CRUD)
- [x] Set up frontend skeleton
- [ ] Implement ingestion (RSS + APIs)
- [ ] Implement LLM pipeline
- [ ] Implement TTS
- [ ] Implement Telegram delivery
- [ ] Set up scheduling
- [ ] Build frontend features
- [ ] Write tests
- [ ] Deploy to production

---

## Resources & References

- FastAPI: https://fastapi.tiangolo.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
- React: https://react.dev/
- OpenAI API: https://platform.openai.com/docs/
- Telegram Bot API: https://core.telegram.org/bots/api
- APScheduler: https://apscheduler.readthedocs.io/
