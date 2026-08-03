"""E2E smoke test over a real HTTP server: full stack + SPA serving."""
import os
import subprocess
import sys
import time

import httpx

PORT = 8765
BASE = f"http://127.0.0.1:{PORT}"
PASSWORD = "Str0ng!Pass"

for stale in ("e2e.db", "e2e_server.log"):
    if os.path.exists(stale):
        os.remove(stale)
import shutil

if os.path.isdir("e2e_storage"):
    shutil.rmtree("e2e_storage")

os.environ["DATABASE_URL"] = "sqlite:///./e2e.db"
os.environ["STORAGE_DIR"] = "./e2e_storage"
os.environ["SECRET_KEY"] = "e2e-secret"
os.environ["PUBLIC_BASE_URL"] = f"http://127.0.0.1:{PORT}"
os.environ["SMTP_HOST"] = ""
os.environ["RATE_LIMIT_ENABLED"] = "false"

LOG_FILE = "e2e_server.log"
if os.path.exists(LOG_FILE):
    os.remove(LOG_FILE)

server = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "app.main:app", "--port", str(PORT)],
    stdout=open(LOG_FILE, "w"),
    stderr=subprocess.STDOUT,
    text=True,
)

failures = []


def check(name, cond, extra=""):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {name} {extra}")
    if not cond:
        failures.append(name)


def wait_ready():
    for _ in range(40):
        try:
            r = httpx.get(f"{BASE}/api/health", timeout=2)
            if r.status_code == 200:
                return
        except Exception:
            pass
        time.sleep(0.5)
    raise SystemExit("server did not start")


try:
    wait_ready()
    c = httpx.Client(base_url=BASE, timeout=10)

    # 1. SPA is served by FastAPI
    r = c.get("/")
    check("SPA index served", r.status_code == 200 and "CareCode" in r.text)
    r = c.get("/login")
    check("SPA deep link served", r.status_code == 200 and "CareCode" in r.text)
    asset = c.get("/assets/").status_code
    check("assets mounted", asset == 404 or asset == 200)

    # 2. Register -> auto profile with carecode
    reg = c.post("/api/v1/auth/register", json={"email": "e2e@example.com", "full_name": "E2E User", "password": PASSWORD})
    check("register", reg.status_code == 201)
    tokens = reg.json()["tokens"]
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}

    # 3. Save profile
    profile = {
        "full_name": "E2E User",
        "date_of_birth": "1990-01-15",
        "gender": "other",
        "blood_group": "B+",
        "allergies": "Latex",
        "conditions": "Asthma",
        "medications": "Inhaler",
        "address": "1 E2E Street",
        "notes": "Test",
        "contacts": [{"name": "Sam", "relationship": "Friend", "phone": "+91 90000 00000"}],
    }
    saved = c.post("/api/v1/users/me/profile", json=profile, headers=headers)
    check("save profile", saved.status_code == 200)
    code = saved.json()["carecode"]

    # 4. QR assets
    png = c.get(f"/api/v1/qr/{code}/image?format=png")
    check("QR PNG", png.status_code == 200 and png.headers["content-type"] == "image/png")
    svg = c.get(f"/api/v1/qr/{code}/image?format=svg")
    check("QR SVG", svg.status_code == 200 and b"<svg" in svg.content)
    card = c.get(f"/api/v1/qr/{code}/card", headers=headers)
    check("printable card", card.status_code == 200 and "CareCode" in card.text)

    # 5. Public page (anonymous)
    pub = c.get(f"/api/v1/public/{code}")
    check("public emergency page", pub.status_code == 200 and pub.json()["blood_group"] == "B+")
    summary = c.get(f"/api/v1/public/{code}/summary")
    check("summary download", summary.status_code == 200 and "Asthma" in summary.text)

    # 6. Analytics
    stats = c.get("/api/v1/analytics/me", headers=headers)
    check("scan analytics", stats.json()["total_scans"] == 1)

    # 7. Forgot password -> console email contains token
    fp = c.post("/api/v1/auth/forgot-password", json={"email": "e2e@example.com"})
    check("forgot password", fp.status_code == 200)
    time.sleep(1.5)
    with open(LOG_FILE, encoding="utf-8", errors="replace") as f:
        log_text = f.read()
    import re

    m = re.search(r"reset-password\?token=([A-Za-z0-9_\-]+)", log_text)
    check("reset email emitted", m is not None)
    token = m.group(1) if m else ""

    rp = c.post("/api/v1/auth/reset-password", json={"token": token, "password": "New!Passw0rd"})
    check("reset password", rp.status_code == 200)
    login_new = c.post("/api/v1/auth/login", json={"email": "e2e@example.com", "password": "New!Passw0rd"})
    check("login with new password", login_new.status_code == 200)

    # 8. Repeated login -> logout -> login cycles (regression: stale refresh/session state)
    cycle_tokens = login_new.json()["tokens"]
    for i in range(1, 4):
        lg = c.post("/api/v1/auth/logout", json={"refresh_token": cycle_tokens["refresh_token"]})
        check(f"cycle {i} logout", lg.status_code == 204)
        li = c.post("/api/v1/auth/login", json={"email": "e2e@example.com", "password": "New!Passw0rd"})
        check(f"cycle {i} re-login", li.status_code == 200)
        cycle_tokens = li.json()["tokens"]
        me = c.get("/api/v1/users/me", headers={"Authorization": f"Bearer {cycle_tokens['access_token']}"})
        check(f"cycle {i} session valid", me.status_code == 200 and me.json()["email"] == "e2e@example.com")

    # 9. Delete account -> QR invalid forever
    # (password reset invalidated the old session — re-login first)
    fresh = c.post("/api/v1/auth/login", json={"email": "e2e@example.com", "password": "New!Passw0rd"})
    check("re-login after reset", fresh.status_code == 200)
    headers = {"Authorization": f"Bearer {fresh.json()['tokens']['access_token']}"}
    dl = c.delete("/api/v1/users/me", params={"password": "New!Passw0rd"}, headers=headers)
    check("delete account", dl.status_code == 204)
    gone = c.get(f"/api/v1/public/{code}")
    check(
        "old QR returns 410 with generic message",
        gone.status_code == 410 and "no longer available" in gone.json()["detail"],
        str(gone.status_code),
    )
    gone_png = c.get(f"/api/v1/qr/{code}/image?format=png")
    check("old QR image 410", gone_png.status_code == 410)
    relogin = c.post("/api/v1/auth/login", json={"email": "e2e@example.com", "password": "New!Passw0rd"})
    check("login after deletion fails", relogin.status_code == 401)

    # 10. Hospitals seeded (expanded static catalog)
    hosp = c.get("/api/v1/hospitals")
    check("hospitals seeded", hosp.json()["total"] > 400, str(hosp.json()["total"]))
    states = c.get("/api/v1/hospitals/states").json()["states"]
    check("states endpoint", len(states) >= 36 and "Tamil Nadu" in states, str(len(states)))
    tamil = c.get("/api/v1/hospitals", params={"state": "Tamil Nadu"}).json()["total"]
    check("TN emphasis", tamil > 80, str(tamil))

    print("\n" + ("ALL E2E CHECKS PASSED" if not failures else f"{len(failures)} FAILURES"))
    sys.exit(1 if failures else 0)
finally:
    server.terminate()
    try:
        server.wait(timeout=5)
    except subprocess.TimeoutExpired:
        server.kill()
