# AI News Broadcaster — Task Board

Legend: `[ ]` not started · `[~]` in progress · `[x]` done

---

## 🗄️ Database
- [ ] Set up SQLAlchemy + Alembic
- [ ] Create `sources` table + model
- [ ] Create `articles` table + model
- [ ] Create `story_clusters` + `article_clusters` tables + models
- [ ] Create `digests` + `digest_articles` tables + models
- [ ] Create `delivery_logs` table + model
- [ ] Create `user_settings` table + model
- [ ] Write first Alembic migration
- [ ] Seed a few test sources (RSS feeds)

## 📰 Ingestion
- [ ] `rss_fetcher.py` — pull + parse RSS feeds (feedparser)
- [ ] `api_fetcher.py` — pull from any API sources (e.g. Hacker News, arXiv)
- [ ] Store raw articles in DB, dedupe by URL

## 🧠 LLM Pipeline (filtering + summarization)
- [ ] `llm_client.py` — GroqClient + GeminiClient behind a common interface, with fallback on error
- [ ] `filter.py` — relevance classification prompt (benchmark / product launch / low-spec model / free tool / not relevant)
- [ ] `summarizer.py` — radio-anchor-style summary prompt
- [ ] `dedup.py` — near-duplicate detection across sources (embeddings or simple similarity)
- [ ] Test the pipeline end-to-end on a batch of real articles

## 🔊 Audio
- [ ] `tts.py` — EdgeTTSClient (primary) + ElevenLabsClient (quality fallback)
- [ ] Generate a test audio file from a sample summary
- [ ] Store audio file path in `digests` table

## 📬 Delivery
- [ ] `telegram_bot.py` — send audio + digest text via Telegram Bot API
- [ ] Create bot with BotFather, store token/chat ID
- [ ] Log delivery status to `delivery_logs`

## ⏰ Scheduling
- [ ] `scheduler.py` — APScheduler job for local dev
- [ ] `/pipeline/run` manual-trigger endpoint (for testing without waiting on cron)
- [ ] GitHub Actions cron workflow for deployed version

## 🖥️ Backend API (FastAPI)
- [ ] Project skeleton + `core/config.py` (pydantic-settings, env vars)
- [ ] `routes/articles.py`
- [ ] `routes/digests.py`
- [ ] `routes/settings.py`
- [ ] `routes/logs.py`
- [ ] Error handling + structured logging across all routes

## 🎨 Frontend (React + Vite)
- [ ] Project skeleton
- [ ] Dashboard — news cards (mock data first)
- [ ] Filter/sort interface
- [ ] Summary view (with audio player)
- [ ] Settings page (Telegram token, schedule time)
- [ ] Wire dashboard to real API endpoints

## 🚀 DevOps / Deployment
- [ ] `.devcontainer/devcontainer.json` for Codespaces
- [ ] `.gitignore` (Python, Node, `.env`, generated audio files)
- [ ] GitHub Actions CI (lint + test on push)
- [ ] Deploy backend to Render
- [ ] Deploy frontend to Vercel
- [ ] Set up Supabase (Postgres) for production DB
- [ ] Store all API keys as GitHub/Render/Vercel secrets — never commit `.env`

## ✅ Testing
- [ ] Unit tests for `filter.py` / `summarizer.py` (mock LLM responses)
- [ ] Integration test for the full pipeline on a small fixture batch
- [ ] Manual test of a full morning run: fetch → filter → summarize → TTS → Telegram
