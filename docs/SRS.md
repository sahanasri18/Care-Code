# CareCode — Software Requirements Specification (SRS)

**Version:** 1.0  
**Status:** Approved  
**Project:** CareCode – Scan. Care. Save Lives.

---

## 1. Introduction

### 1.1 Purpose
CareCode is a digital emergency medical identification platform. Users securely store
essential medical information and share it instantly during emergencies via a QR code.
Any smartphone can scan the QR code and view a public emergency page — no login required.

### 1.2 Scope
- Account management (register, login, logout, password recovery)
- Emergency medical profile management
- QR code generation, regeneration, download (PNG/SVG), and printing
- Public emergency page (no authentication)
- Hospital directory (search, nearby, details)
- Scan analytics and user activity
- Administrative dashboard (user & hospital management, analytics)
- Account deletion with full GDPR-style data cleanup and permanent QR invalidation

### 1.3 Definitions
| Term | Definition |
|---|---|
| Medical Profile | The user's emergency health record (blood group, allergies, conditions, etc.) |
| CareCode / QR | Unique scannable identifier pointing to a public emergency page |
| Emergency Page | Public, unauthenticated page showing emergency-relevant data only |
| Responder | Doctor, paramedic, first responder, or bystander scanning the QR |

---

## 2. Overall Description

### 2.1 Actors
| Actor | Description |
|---|---|
| Anonymous visitor | Scans QR / views public emergency page, searches hospitals |
| User | Registered account holder; manages profile and QR |
| Admin | Manages users, hospitals; views analytics |

### 2.2 User Stories
1. As a user, I can register and log in so that my medical data is protected.
2. As a user, I can create/edit my emergency medical profile (name, DOB, gender, blood group, allergies, conditions, medications, emergency contacts, address, notes, photo).
3. As a user, I can download/print my QR code so that I can place it on cards, bracelets, helmets, or keychains.
4. As a responder, I can scan any CareCode and instantly see emergency-relevant information without logging in.
5. As a responder, I can call emergency contacts directly from the emergency page and download a medical summary.
6. As a user, I can recover my password via a secure, time-limited, single-use email link.
7. As a user, I can permanently delete my account; afterwards, scanning my old QR shows a neutral "profile unavailable" message and never leaks data.
8. As a user, I can find and view nearby hospitals.
9. As an admin, I can manage application resources (hospitals) and view aggregate platform analytics — but never access any user's account or medical data.

### 2.3 Functional Requirements

#### FR-1 Authentication
- FR-1.1 Register with email + password; email must be unique and valid; password strength enforced (min 8 chars, upper, lower, digit, symbol).
- FR-1.2 Login with email + password; issue short-lived access JWT and refresh token.
- FR-1.3 Logout revokes the active token server-side.
- FR-1.4 Refresh tokens renew access without re-login; revoked tokens are rejected.
- FR-1.5 Change password requires the current password; invalidates other sessions.
- FR-1.6 Forgot password: enter email → system verifies existence (no user enumeration) → generates single-use token valid 30 minutes → sends branded HTML email with reset link.
- FR-1.7 Reset password: valid token → validate new password strength → hash and store → invalidate token (single-use) → redirect to login.

#### FR-2 Medical Profile
- FR-2.1 Create/edit profile: full name, date of birth, gender, blood group, allergies, conditions, medications, emergency contacts (name, relationship, phone), address, notes, optional photo.
- FR-2.2 Photo upload (JPEG/PNG/WebP, ≤ 5 MB), stored securely; served only through authenticated endpoints except an anonymized thumbnail on the emergency page.
- FR-2.3 One profile per user; only the owner may edit it.

#### FR-3 QR Management
- FR-3.1 A unique CareCode is generated automatically with the profile.
- FR-3.2 Regenerate QR: new code generated; the previous code becomes permanently invalid.
- FR-3.3 Download PNG, Download SVG, Print (browser print of a QR card).
- FR-3.4 QR encodes a URL to the public emergency page (`/e/{code}`).

#### FR-4 Public Emergency Page
- FR-4.1 Accessible without authentication; loads fast; mobile-first.
- FR-4.2 Shows: name, age, photo, blood group, allergies, conditions, medications, emergency contacts with tap-to-call, address, notes, and a clear medical-alert design.
- FR-4.3 Download Medical Summary (PDF-style printable view or text card).
- FR-4.4 Each visit increments the scan counter (rate-limited per code).
- FR-4.5 Deleted/regenerated codes return HTTP 410 with a generic, professional "profile no longer available" page — no personal data, no reason given.

#### FR-5 Hospitals
- FR-5.1 Search hospitals by name/department/city.
- FR-5.2 Nearby hospitals sorted by distance (haversine) with optional device geolocation.
- FR-5.3 Hospital detail view (address, phone, departments, coordinates).
- FR-5.4 Static seed dataset (537 hospitals, all states/UTs, TN emphasis) ships with the app and loads on first boot — no external APIs.

#### FR-6 Analytics
- FR-6.1 Scan count per user profile (total, last 30 days).
- FR-6.2 Activity log (login, profile update, QR regeneration, password change, deletion).
- FR-6.3 Admin platform statistics (users, scans, hospitals, growth).

#### FR-7 Admin
- FR-7.1 No admin access to user accounts or medical profiles — privacy-first; all account actions are self-service via Account Settings.
- FR-7.2 Manage hospitals (create, edit, delete).
- FR-7.3 Analytics dashboard with aggregate platform KPIs only (no per-user or personal data).

#### FR-8 Account Deletion
- FR-8.1 User navigates to Account Settings → Delete Account.
- FR-8.2 Confirmation dialog warns the action is permanent.
- FR-8.3 Password must be re-entered and verified before deletion.
- FR-8.4 Deletion removes: user, medical profile, emergency contacts, profile photo files, QR records, scan analytics, activity logs, refresh tokens.
- FR-8.5 Old QR codes permanently return the "unavailable" page (HTTP 410); nothing personal is disclosed.

### 2.4 Non-Functional Requirements
| Requirement | Detail |
|---|---|
| Security | bcrypt password hashing; JWT access (30 min) + refresh (7 days); HTTPS; no secrets in code; env vars only; CORS restricted; rate limiting on auth + scans |
| Performance | Emergency page returns < 300 ms; static assets cached; no N+1 queries |
| Availability | Stateless API; deployable on Render; PostgreSQL for persistence |
| Portability | SQLAlchemy models run on PostgreSQL (prod) and SQLite (dev/test) |
| Maintainability | Modular clean architecture; typed Pydantic schemas; Alembic migrations |
| Accessibility | WCAG AA contrast; semantic HTML; keyboard operable |
| Privacy | Public page shows only emergency-relevant data; deletion is irreversible and complete |

---

## 3. Assumptions & Constraints
- Deployment target: Render (web service + managed PostgreSQL).
- Email: SMTP (Gmail/other) configured via environment variables; a console email backend is used when SMTP is unset (dev/test) and the reset link is logged.
- No real-time messaging or native mobile apps in v1.

## 4. Acceptance Criteria (key flows)
- AC-1 Register → login → create profile → QR appears → download PNG/SVG works → print view opens.
- AC-2 Logout then scan QR (anonymous) → emergency page renders full emergency info + call buttons.
- AC-3 Forgot password → email with link → reset → login with new password works; token reuse fails; expired token fails.
- AC-4 Delete account → old QR returns 410 "no longer available" page; no data leak; token invalidated.
- AC-5 Admin endpoints expose no user data: no /admin/users routes exist; /admin/stats returns aggregate numbers only.
- AC-6 All backend flows pass pytest suite; frontend passes production build.
