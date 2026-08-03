# CareCode — Database Schema Design

**Engine:** PostgreSQL (production) / SQLite (dev, test). Dialect-agnostic DDL via SQLAlchemy + Alembic.

![ERD summary]

```
users ──1:1── medical_profiles ──1:N── emergency_contacts
  │                │
  │                └──1:N── scan_events
  │
  ├──1:N── activity_logs
  ├──1:N── revoked_tokens
  └──1:N── password_reset_tokens

hospitals (standalone catalog)
```

---

## users

| Column | Type | Constraints |
|---|---|---|
| id | UUID PK | default uuid4 |
| email | String(255) | unique, not null, lowercase |
| password_hash | String(255) | not null |
| full_name | String(120) | not null |
| role | String(20) | default `user` (`user`/`admin`) |
| is_active | Boolean | default true (admin deactivation) |
| email_verified | Boolean | default false (reserved for future) |
| created_at | DateTime(tz) | server default |
| updated_at | DateTime(tz) | onupdate |

- Email login only. `role` gates admin routes.
- `is_active=false` → login and QR public page both disabled.

## medical_profiles

| Column | Type | Constraints |
|---|---|---|
| id | UUID PK | |
| user_id | UUID FK→users | unique, not null, cascade delete |
| carecode | String(36) | unique, indexed, not null (UUID4) |
| full_name | String(120) | not null |
| date_of_birth | Date | nullable |
| gender | String(20) | nullable (enum-ish value list) |
| blood_group | String(5) | nullable (A+, A-, B+, B-, AB+, AB-, O+, O-) |
| allergies | Text | nullable |
| conditions | Text | nullable |
| medications | Text | nullable |
| address | Text | nullable |
| notes | Text | nullable |
| photo_filename | String(255) | nullable (stored file on disk) |
| scan_count | Integer | default 0 (denormalized for speed) |
| last_scanned_at | DateTime(tz) | nullable |
| created_at / updated_at | DateTime(tz) | |

- `carecode` is the QR payload segment; regeneration replaces it (old value no longer resolves).
- Deletion of profile cascades: contacts, scan events.

## emergency_contacts

| Column | Type | Constraints |
|---|---|---|
| id | UUID PK | |
| profile_id | UUID FK→medical_profiles | cascade delete |
| name | String(120) | not null |
| relationship | String(60) | not null |
| phone | String(30) | not null |

## password_reset_tokens

| Column | Type | Constraints |
|---|---|---|
| id | UUID PK | |
| user_id | UUID FK→users | cascade delete |
| token_hash | String(64) | unique, SHA-256 of raw token (never stored raw) |
| expires_at | DateTime(tz) | not null |
| used_at | DateTime(tz) | nullable (single-use) |
| created_at | DateTime(tz) | |

- Lookup is by token_hash only. Used/expired tokens rejected; single-use enforced with `used_at IS NULL`.

## revoked_tokens

| Column | Type | Constraints |
|---|---|---|
| id | UUID PK | |
| jti | String(36) | unique, not null |
| expires_at | DateTime(tz) | not null (purge-friendly) |
| created_at | DateTime(tz) | |

- JWT carries `jti`; logout/global invalidation inserts jti → auth middleware rejects.

## activity_logs

| Column | Type | Constraints |
|---|---|---|
| id | BigInt PK autoincrement | |
| user_id | UUID FK→users | null on delete (audit retained? No — GDPR: user rows removed) → cascade delete |
| action | String(60) | e.g. `login`, `profile_update`, `qr_regenerate`, `password_change` |
| detail | JSON | nullable |
| created_at | DateTime(tz) | |

## scan_events

| Column | Type | Constraints |
|---|---|---|
| id | BigInt PK autoincrement | |
| profile_id | UUID FK→medical_profiles | cascade delete |
| ip_hash | String(64) | SHA-256 of IP (privacy: no raw IP stored) |
| user_agent | String(255) | nullable |
| created_at | DateTime(tz) | |

- Used for scan analytics; denormalized `scan_count` on profile kept in sync.

## hospitals

| Column | Type | Constraints |
|---|---|---|
| id | UUID PK | |
| name | String(200) | not null |
| address | String(300) | not null |
| city | String(100) | not null, indexed |
| state | String(50) | not null, indexed |
| pincode | String(10) | nullable |
| phone | String(30) | nullable |
| latitude | Float | not null |
| longitude | Float | not null |
| departments | JSON | list of strings |
| created_at | DateTime(tz) | |

The catalog ships as a static file (`backend/app/data/hospitals.json`, 537 hospitals,
all 36 states/UTs, Tamil Nadu emphasis) and is loaded on first boot when the table is
empty. Regenerate with `python -m scripts.build_hospital_seed`.

---

## Indexes
- `medical_profiles.carecode` (unique) — QR lookup hot path
- `medical_profiles.user_id` (unique)
- `password_reset_tokens.token_hash` (unique)
- `password_reset_tokens.user_id`
- `revoked_tokens.jti` (unique)
- `hospitals.city`
- `hospitals.state`
- `scan_events.profile_id`

## Data retention
- Deletion removes all user-derived rows (cascade): profiles, contacts, reset tokens, revoked tokens, activity logs, scan events, photo file. Hospital catalog is shared, non-personal data.
