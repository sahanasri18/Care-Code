# CareCode — Architecture & Folder Structure

## High-level architecture

```
┌─────────────────────────┐         HTTPS          ┌──────────────────────────┐
│  React SPA (Vite)       │ ─────────────────────► │  FastAPI (Render)        │
│  - Public emergency page│   /api/v1  (Bearer JWT)│  - API routers /api/v1    │
│  - Auth/Dashboard/Admin │                        │  - Services (email, qr)   │
└─────────────────────────┘                        │  - SQLAlchemy ORM         │
        ▲                                          └───────────┬──────────────┘
        │  static build served by FastAPI on Render            │
        └──────────────────────────────────────────────────────▼
                                                   ┌──────────────────────────┐
                                                   │ PostgreSQL (Render)      │
                                                   │  + filesystem (photos)   │
                                                   └──────────────────────────┘
```

- Single Render web service: FastAPI serves `/api/v1` and the built React SPA (production).
- Dev: Vite dev server proxies `/api` → `http://localhost:8000`.

## Layering (backend)

```
app/
├── main.py               # FastAPI app, CORS, routers, static SPA mount
├── core/
│   ├── config.py         # pydantic-settings; all env vars here — zero hardcoded URLs
│   ├── database.py       # engine, SessionLocal, get_db
│   ├── security.py       # bcrypt, JWT create/verify, jti handling, token hashing
│   ├── email.py          # SMTP sender + console fallback + HTML templates
│   ├── qr.py             # QR PNG/SVG generation
│   └── rate_limit.py     # in-memory sliding-window limiter
├── models/               # SQLAlchemy models (users, profiles, hospitals, ...)
├── schemas/              # Pydantic v2 request/response schemas
├── api/
│   ├── deps.py           # get_db, get_current_user, require_admin
│   └── v1/               # routers: auth, users, qr, public, hospitals, analytics, admin
├── services/             # business logic: auth_service, profile_service, deletion, hospital_seed
└── utils/                # pagination helper
tests/                    # pytest (full flows, in-memory SQLite)
alembic/                  # migrations
```

## Frontend structure

```
frontend/src/
├── main.jsx              # entry, BrowserRouter
├── App.jsx               # route table + guards
├── api/client.js         # axios instance + interceptors (auto refresh, 401 → login)
├── context/AuthContext.jsx
├── components/           # Button, Input, Card, Modal, Spinner, Navbar, Footer, Layout
├── pages/
│   ├── auth/       Login, Register, ForgotPassword, ResetPassword
│   ├── dashboard/  Dashboard, ProfileEditor, QRManager, AccountSettings
│   ├── public/     EmergencyPage (no auth)
│   ├── hospitals/  Hospitals, HospitalDetail
│   └── admin/      AdminDashboard, AdminHospitals (no user management — privacy-first)
└── utils/          format.js (age calc, date fmt)
```

## Design principles
1. **No hardcoded URLs** — `VITE_API_URL`, `VITE_PUBLIC_BASE_URL` env vars; API base from `import.meta.env`.
2. **No duplicated logic** — shared core services; routers are thin.
3. **Security first** — bcrypt, hashed reset tokens, jti revocation, no raw IP storage, no enumeration on forgot-password, 410 on deleted codes.
4. **Portable DB** — SQLAlchemy models avoid PG-only types → SQLite for tests, PostgreSQL in prod.
5. **Defense in depth** — Pydantic validation + ORM-level constraints + route-level auth checks.

## Environments
| Env | DB | Email | Notes |
|---|---|---|---|
| dev | `sqlite:///./carecode.db` | console (logs link) | `uvicorn app.main:app --reload` |
| test | `sqlite:///:memory:` | console | pytest fixtures |
| prod (Render) | `DATABASE_URL` (Postgres) | SMTP env | alembic upgrade on deploy |

## Configuration surface (env)
`SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `REFRESH_TOKEN_EXPIRE_DAYS`,
`DATABASE_URL`, `FRONTEND_URL`, `SMTP_HOST/PORT/USER/PASSWORD/FROM/TLS`,
`RESET_TOKEN_EXPIRE_MINUTES`, `STORAGE_DIR`, `VITE_API_URL`, `VITE_PUBLIC_BASE_URL`.
