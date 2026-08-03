# CareCode — Development Roadmap

Each phase ends with verification; no phase starts until the previous is green.

## Phase 0 — Planning ✅
- SRS, DB schema, API design, architecture, wireframes (docs/).

## Phase 1 — Backend foundation
1. Scaffold FastAPI project, config (pydantic-settings), database, security (bcrypt + JWT), rate limiter.
2. SQLAlchemy models + Alembic (initial migration).
3. Verify: app boots; health endpoint; migration applies cleanly.

## Phase 2 — Authentication
4. Register / Login / Refresh / Logout / Change password.
5. **Forgot / Reset password**: hashed single-use tokens, expiry, HTML email, console fallback.
6. Verify: pytest auth suite (register, login, wrong password, refresh, logout revocation, password strength, reset flow incl. reuse/expiry).

## Phase 3 — Medical profile
7. Profile upsert + contacts + photo upload/remove.
8. Verify: pytest profile suite.

## Phase 4 — QR & public page
9. QR generation (PNG/SVG), regeneration, printable card, public emergency page, scan tracking with rate limit, summary download.
10. Verify: pytest public suite; old code → 410 after regeneration.

## Phase 5 — Account deletion
11. Delete account (password-confirmed) with full cascade cleanup + photo file removal + token invalidation; admin deactivation.
12. Verify: pytest deletion suite — after deletion: old QR → 410, login fails, token rejected, no orphan rows, photo file gone.

## Phase 6 — Hospitals & analytics
13. Hospitals CRUD + seed data, search/nearby/detail; per-user analytics endpoint.
14. Verify: pytest hospitals + analytics suite.

## Phase 7 — Admin
15. Admin hospitals/stats endpoints; role enforcement; no user-management endpoints (privacy-first).
16. Verify: pytest admin suite (non-admin 403).

## Phase 8 — Frontend foundation
17. Vite + React + Tailwind + Router + axios client (refresh interceptor) + AuthContext + guards + layout/components.
18. Verify: `npm run build` green; login/register flows work against backend.

## Phase 9 — Frontend features
19. Auth pages (incl. Forgot/Reset with strength meter).
20. Dashboard + Profile editor + QR manager (download/print/regenerate) + Account settings (change password + delete flow with modal).
21. Public emergency page (mobile-first, call buttons, summary, 410 state).
22. Hospitals + Admin pages.
23. Verify: full end-to-end manual test script + production build.

## Phase 10 — Deployment & QA
24. Render config (render.yaml, build scripts, alembic migration on start), .env examples, README.
25. Final QA: test matrix execution, docs review, secrets audit, performance sanity.
