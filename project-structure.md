ai-news-broadcaster/
├── .devcontainer/
│   └── devcontainer.json
├── .github/
│   └── workflows/
│       └── ci.yml
├── frontend/                      # UI — React + Vite
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── NewsCard.jsx
│   │   │   ├── FilterBar.jsx
│   │   │   ├── SummaryView.jsx
│   │   │   └── SettingsForm.jsx
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx
│   │   │   └── Settings.jsx
│   │   ├── mock/
│   │   │   └── mockArticles.json
│   │   ├── api/
│   │   │   └── client.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── backend/                       # API layer only — FastAPI routes + orchestration
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── articles.py
│   │   │       ├── digests.py
│   │   │       ├── settings.py
│   │   │       ├── logs.py
│   │   │       └── pipeline.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── logging.py
│   │   └── main.py
│   ├── requirements.txt
│   └── tests/
│
├── services/                       # business logic — ingestion, LLM pipeline, audio, delivery, scheduling
│   ├── ingestion/
│   │   ├── rss_fetcher.py
│   │   └── api_fetcher.py
│   ├── pipeline/
│   │   ├── llm_client.py
│   │   ├── filter.py
│   │   ├── summarizer.py
│   │   └── dedup.py
│   ├── audio/
│   │   └── tts.py
│   ├── delivery/
│   │   └── telegram_bot.py
│   └── scheduling/
│       └── scheduler.py
│
├── db/                              # models, migrations, session handling
│   ├── models/
│   │   ├── source.py
│   │   ├── article.py
│   │   ├── story_cluster.py
│   │   ├── digest.py
│   │   ├── delivery_log.py
│   │   └── user_settings.py
│   ├── migrations/                 # Alembic
│   │   └── versions/
│   ├── alembic.ini
│   └── session.py
│
├── .env.example
├── .gitignore
├── TASKS.md
├── README.md
└── ai-news-broadcaster-plan.md