# CareCode — API Design (v1)

Base URL: `/api/v1` · All JSON. Auth: `Authorization: Bearer <access_token>`.

## Conventions
- Errors: `{"detail": "message"}` (FastAPI standard). Validation errors: `422` with field details.
- Pagination: `?page=1&page_size=20` → `{"items": [...], "total": n, "page": p, "page_size": s}`.
- Codes: `410 Gone` for deleted/regenerated CareCodes.

## Auth
| Method | Path | Access | Body → Response |
|---|---|---|---|
| POST | /auth/register | public | `{email, password, full_name}` → `201 {user, access_token, refresh_token}` |
| POST | /auth/login | public | `{email, password}` → `{user, access_token, refresh_token}` |
| POST | /auth/refresh | public | `{refresh_token}` → `{access_token, refresh_token}` |
| POST | /auth/logout | auth | `{refresh_token}` → `204` (revokes refresh jti) |
| POST | /auth/forgot-password | public | `{email}` → always `200 {message}` (no enumeration) |
| POST | /auth/reset-password | public | `{token, password}` → `200 {message}` (single use) |
| POST | /auth/change-password | auth | `{current_password, new_password}` → `200` (revokes other sessions) |

## Users
| Method | Path | Access | Notes |
|---|---|---|---|
| GET | /users/me | auth | current user |
| GET | /users/me/profile | auth | medical profile incl. contacts |
| POST | /users/me/profile | auth | create/update profile (upsert) |
| PUT | /users/me/profile/photo | auth (multipart) | upload photo |
| DELETE | /users/me/profile/photo | auth | remove photo |
| DELETE | /users/me | auth | `{password}` → full deletion (204) |
| POST | /users/me/regenerate-qr | auth | new carecode, old invalid → `{carecode, qr_url}` |

## QR Assets
| Method | Path | Access | Notes |
|---|---|---|---|
| GET | /qr/{code}/image?format=png\|svg | public | returns file (`image/png` or `image/svg+xml`) |
| GET | /qr/{code}/card | auth (owner) | printable HTML card (browser print) |

## Public Emergency
| Method | Path | Access | Notes |
|---|---|---|---|
| GET | /public/{code} | public | emergency data; increments scan counter (rate-limited) |
| GET | /public/{code}/photo | public | anonymized profile photo (or 404) |
| GET | /public/{code}/summary | public | downloadable medical summary (text/HTML) |

Scan of invalid/deleted code → `410` with generic message.

## Hospitals
| Method | Path | Access | Notes |
|---|---|---|---|
| GET | /hospitals | public | `?q=&city=&state=&page=` |
| GET | /hospitals/cities | public | distinct cities |
| GET | /hospitals/states | public | distinct states |
| GET | /hospitals/nearby | public | `?lat=&lng=&radius_km=` haversine sorted |
| GET | /hospitals/{id} | public | details |

## Analytics
| Method | Path | Access | Notes |
|---|---|---|---|
| GET | /analytics/me | auth | scan_count, last_30_days, activity log |

## Admin
Privacy-first: the admin API manages only application resources. There are no
user-management endpoints — accounts and medical data are strictly self-service.

| Method | Path | Access | Notes |
|---|---|---|---|
| GET | /admin/hospitals | admin | paginate |
| POST | /admin/hospitals | admin | create |
| PUT | /admin/hospitals/{id} | admin | update |
| DELETE | /admin/hospitals/{id} | admin | delete |
| GET | /admin/stats | admin | aggregate platform analytics only (users, scans, hospitals, signups per day) — never per-user data |

## Security
- Access JWT: 30 min; Refresh JWT: 7 days; both HS256, `jti` claim; refresh also revocable.
- Passwords: bcrypt (12 rounds) — stored hashed only.
- Reset tokens: 128-bit random, stored SHA-256, expire 30 min, single use.
- Rate limits: login 10/min/IP, forgot-password 3/hour/IP, public scan 30/min/code.
- CORS: `FRONTEND_URL` env; credentials not required (Bearer).
