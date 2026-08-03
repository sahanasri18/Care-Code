# CareCode — UI Wireframes (low fidelity)

Design language: clean medical UI — white surfaces, deep blue primary (#0B5FFF),
red medical-accent (#E11D48) for emergency context, rounded-2xl cards, Inter typeface,
mobile-first. Emergency page uses high-contrast red header for instant recognition.

---

## 1. Register / Login / Forgot / Reset (auth)
```
┌──────────────────────────────┐
│  ◉ CareCode                  │
│  ────────────────────────    │
│  Email     [              ]  │
│  Password  [••••••••      ]  │
│  [  Sign In  ]               │
│  Forgot Password?  · Register│
│  ------------------------    │
│  "Scan. Care. Save Lives."   │
└──────────────────────────────┘
```
- Forgot: email field → success panel ("If an account exists, a reset link was sent.").
- Reset: new password + confirm with strength meter → success → redirect to login.

## 2. Dashboard
```
┌── Navbar: CareCode | Dashboard Profile QR Hospitals Admin ●avatar──┐
│ ┌─────────────┐  ┌──────────────────────────────┐                   │
│ │ 👤 Name     │  │ Scan activity                │                   │
│ │ Blood: O+   │  │ Total scans   Last 30 days   │                   │
│ │ [QR card]   │  │   128             42         │                   │
│ │ [View QR]   │  │ ── activity log ──           │                   │
│ └─────────────┘  │ • login  Aug 3               │                   │
│                  │ • profile updated  Aug 2     │                   │
│                  └──────────────────────────────┘                   │
└─────────────────────────────────────────────────────────────────────┘
```

## 3. Profile Editor
```
┌────────────────────────────────────────┐
│ Photo [◉] upload / remove              │
│ Full name [____________]   DOB [______]│
│ Gender [select]   Blood group [select] │
│ Allergies [textarea]                   │
│ Conditions [textarea]                  │
│ Medications [textarea]                 │
│ Address [textarea]  Notes [textarea]   │
│ ─ Emergency contacts ─                 │
│ Name [____] Relation [____] Phone [____]  [+] [×]│
│ [ Save Profile ]                       │
└────────────────────────────────────────┘
```

## 4. QR Manager
```
┌──────────────────────────────┐
│  [ QR image 300×300 ]        │
│  Code: a1b2…-…-…  (Copy)     │
│  Public URL: https://…/e/…   │
│  [Download PNG] [Download SVG]│
│  [Print Card]  [Regenerate ⚠]│
│  ⚠ Regenerating invalidates   │
│    the current QR forever.    │
└──────────────────────────────┘
```

## 5. Public Emergency Page (mobile-first)
```
┌──────────────────────────────┐
│ 🚨 MEDICAL PROFILE — SCAN   │  (red band)
│ ┌────────────────────────┐  │
│ │ [photo]  Alex Morgan    │  │
│ │          Age 34 · F     │  │
│ │          Blood: O+      │  │
│ └────────────────────────┘  │
│ ALLERGIES                   │
│ Penicillin — severe         │
│ CONDITIONS                  │
│ Type 1 Diabetes             │
│ MEDICATIONS                 │
│ Insulin (daily)             │
│ EMERGENCY CONTACTS          │
│ [📞 Call Sam Morgan]        │
│ [📞 Call Dr. Lee]           │
│ ADDRESS / NOTES             │
│ [Download Summary]          │
└──────────────────────────────┘
```
Deleted/invalid code page:
```
┌──────────────────────────────┐
│  ⚠ CareCode                  │
│  This CareCode profile is    │
│  no longer available.        │
│  The owner has deleted or    │
│  deactivated this emergency  │
│  profile.                    │
└──────────────────────────────┘
```

## 6. Hospitals
List with search box + city filter → cards (name, city, depts, phone) →
detail page with map link. "Nearby" tab uses geolocation → sorted by distance.

## 7. Admin
Tabs: Overview (KPI cards: users, scans, hospitals, signups chart) ·
Hospitals (table + CRUD modal).
Privacy-first: no user management — accounts and medical data are strictly
self-service via each user's Account Settings page.

## 8. Account Settings
Change password form · Danger zone card:
```
┌──────────────────────────────┐
│ ⚠ Delete Account             │
│ This permanently removes…    │
│ [ Delete Account ]           │
│  → modal: enter password     │
│    [Confirm Delete]          │
└──────────────────────────────┘
```
