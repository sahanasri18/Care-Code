# CareCode — Scan. Care. Save Lives.

CareCode is a production-ready **emergency medical identification platform**. Users store
their essential medical information securely and share it instantly during emergencies via a
QR code. Anyone scanning the QR from any smartphone sees a fast, mobile-friendly emergency
page — **no app, no login** — with the exact information a responder needs (blood group,
allergies, conditions, medications, emergency contacts with tap-to-call).

![Stack](https://img.shields.io/badge/Frontend-React%20%2B%20Vite%20%2B%20Tailwind-0B5FFF)
![Stack](https://img.shields.io/badge/Backend-FastAPI%20%2B%20PostgreSQL-0B5FFF)
![Tests](https://img.shields.io/badge/tests-82%20passed-green)

---

## Features

| Area | Capabilities |
|---|---|
| **Auth** | Register, login, logout (server-side token revocation), refresh tokens, change password, full forgot/reset-password flow (SMTP email, single-use 30-minute tokens) |
| **Medical profile** | Name, DOB, gender, blood group, allergies, conditions, medications, address, notes, photo upload, up to 10 emergency contacts |
| **QR** | Auto-generated unique CareCode; download PNG/SVG, printable wallet card, regenerate (old QR permanently invalid) |
| **Emergency page** | Public, mobile-first, medical-alert design, tap-to-call buttons, downloadable medical summary |
| **Hospitals** | 537 offline hospitals across all 36 states/UTs (Tamil Nadu emphasis: 93), shipped as a static seed file — no external APIs; search by name/city/state, nearby via geolocation (haversine), detail pages |
| **Analytics** | Scan counts (total/30-day), activity log per user |
| **Admin** | Privacy-first: manages only hospitals and aggregate platform analytics; no access to user accounts or medical data |
| **Account deletion** | GDPR-style irreversible deletion with full data cleanup; old QR codes permanently return a generic 410 "profile no longer available" page |

## Security highlights

- bcrypt (12 rounds) password hashing — passwords are never stored in plain text
- Short-lived access JWT (30 min) + revocable refresh JWT (7 days); jti blacklist on logout
- Reset tokens: 128-bit random, stored as SHA-256, single use, expire in 30 minutes
- No user enumeration on forgot-password (identical response for known/unknown emails)
- Rate limiting on login, forgot-password and QR scans
- Only IP **hashes** stored for scan analytics (no raw IPs)
- Deleted accounts: cascading removal of profile, contacts, photos, QR, analytics, tokens

## Tech stack

- **Frontend:** React 18, Vite, Tailwind CSS 3, React Router 6, Axios (auto token refresh)
- **Backend:** FastAPI, SQLAlchemy 2, Alembic, Pydantic v2, PyJWT, bcrypt, qrcode
- **Database:** PostgreSQL (production) / SQLite (local dev & tests)
- **Deployment:** Render (web service + managed PostgreSQL, blueprint included)

## Repository layout

```
carecode/
├── docs/                 # SRS, database schema, API design, architecture, wireframes, roadmap
├── backend/
│   ├── app/
│   │   ├── core/         # config, database, security, email, qr, rate_limit
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── api/v1/       # routers: auth, users, qr, public, hospitals, analytics, admin
│   │   ├── services/     # account deletion, profile upsert, activity, hospital seed
│   │   ├── cli.py        # python -m app.cli create-admin ...
│   │   └── main.py       # FastAPI app + SPA serving
│   ├── alembic/          # migrations (initial schema included)
│   ├── tests/            # 82 pytest tests
│   └── requirements.txt
├── frontend/
│   └── src/              # React app (pages, components, context, api client)
├── render.yaml           # Render Blueprint (one-click deploy)
└── .gitignore
```

---

## Local development

### Prerequisites
Python 3.11+, Node 18+

### 1. Backend

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate          # Windows
# source .venv/bin/activate       # macOS / Linux
pip install -r requirements.txt

cp .env.example .env              # then edit as needed (SQLite is the default)
python -m alembic upgrade head    # apply migrations
python run.py                     # uvicorn on http://localhost:8000
```

API docs (Swagger UI): http://localhost:8000/docs

### 2. Frontend

```bash
cd frontend
npm install
npm run dev                       # Vite on http://localhost:5173 (proxies /api → :8000)
```

### 3. Admin account

```bash
cd backend
.\.venv\Scripts\python.exe -m app.cli create-admin admin@example.com "Admin" "Admin1!Pass"
```

### 4. Run the test suite

```bash
cd backend
python -m pip install pytest httpx
python -m pytest tests -q         # 82 tests — auth, reset flow, QR, deletion, admin, hospitals
```

End-to-end smoke test against a real HTTP server:

```bash
cd backend
python scripts/e2e_smoke.py       # boots uvicorn, exercises the full product flow
```

---

## Email (Forgot Password)

The reset-password flow is fully wired end-to-end:

1. User requests a reset → a **single-use token hashed (SHA-256)** in the DB, valid 30 minutes.
2. A branded **HTML email** with a "Reset Password" button is sent via SMTP.
3. The link opens the SPA's Reset Password page; new password is validated for strength.
4. Token is invalidated on use or expiry; old sessions are invalidated; user logs in with the new password.

| Environment | Configuration |
|---|---|
| **Dev / tests** | `SMTP_HOST` empty → emails are logged to the console (link visible in server output) |
| **Production** | Set `SMTP_HOST/PORT/USER/PASSWORD/FROM_EMAIL`. Gmail example: `SMTP_HOST=smtp.gmail.com`, port 587, TLS on, using an [App Password](https://support.google.com/accounts/answer/185833). |

## Deployment (Render)

**Option A — Blueprint (recommended):** push this repo to GitHub, then in Render:
*New Blueprint Instance* → select the repo. `render.yaml` creates the PostgreSQL database,
installs dependencies, builds the frontend, runs Alembic migrations, and starts the API.
Then fill in the four `sync: false` env vars (`FRONTEND_URL`, `PUBLIC_BASE_URL`,
`SMTP_HOST/USER/PASSWORD`, `SMTP_FROM_EMAIL`).

**Option B — Manual:**
- Web service (Python): root dir `/`, build `cd frontend && npm ci && npm run build && cd .. && pip install -r backend/requirements.txt`, start `cd backend && alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Add a managed PostgreSQL database and set `DATABASE_URL`
- Set `SECRET_KEY`, `ENVIRONMENT=production`, `FRONTEND_URL`, `PUBLIC_BASE_URL`, SMTP vars
- Run the smoke test against the deployed URL to verify the full flow

> **Storage note:** profile photos are stored on the service's disk (`STORAGE_DIR`). On Render's
> free/standard plans the disk is ephemeral across deploys; for durable photo storage add an
> S3-compatible bucket and point `STORAGE_DIR` at a mounted volume.

## Environment variables

| Variable | Purpose | Default |
|---|---|---|
| `SECRET_KEY` | JWT signing secret (use a long random value in prod) | — |
| `DATABASE_URL` | SQLAlchemy DB URL | `sqlite:///./carecode.db` |
| `ENVIRONMENT` | `development`/`test`/`production` | `development` |
| `FRONTEND_URL` | CORS allowed origin(s), comma-separated | `http://localhost:5173` |
| `PUBLIC_BASE_URL` | Origin embedded in QR codes & reset emails | empty |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime | 30 |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token lifetime | 7 |
| `RESET_TOKEN_EXPIRE_MINUTES` | Reset link lifetime | 30 |
| `STORAGE_DIR` | Photo storage directory | `./storage` |
| `SMTP_HOST/USER/PASSWORD/FROM_EMAIL/FROM_NAME/PORT/USE_TLS` | Email delivery | empty → console |
| `RATE_LIMIT_ENABLED` | Toggle rate limiting | true |

Frontend (`.env`): `VITE_API_URL` (leave empty in dev — the Vite proxy handles `/api`),
`VITE_PUBLIC_BASE_URL`.

## Documentation

Detailed design documents live in [`docs/`](docs/): SRS, database schema, API contract,
architecture, UI wireframes, and the development roadmap.
