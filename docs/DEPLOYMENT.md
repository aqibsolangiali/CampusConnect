# Deploy CampusConnect on Render

> These settings are tailored to the existing two-service repository layout. The backend and frontend are deployed **separately**.

## 1. Backend: Python Web Service

In Render: **New → Web Service → GitHub repository `CampusConnect`**.

| Setting | Value |
| :--- | :--- |
| Runtime | Python |
| Branch | `main` |
| Root Directory | `backend` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |

Add environment variables:

| Key | Value |
| :--- | :--- |
| `SECRET_KEY` | Your own long, random, **private** value (not a value from this guide) |
| `CORS_ORIGINS` | `https://campusconnect-web-mvbs.onrender.com` |
| `DATABASE_URL` | A durable Postgres connection URL **if** persistent accounts/enrollments are required |

Create a secret locally using `python -c "import secrets; print(secrets.token_urlsafe(48))"` and paste it into the Render **backend environment**, not GitHub or frontend variables.

> Warning: the app falls back to local SQLite when `DATABASE_URL` is absent. On hosts with ephemeral filesystems, accounts/enrollments/bookmarks can disappear after restarts or deploys. The demo is not production-grade without persistence and stronger security controls.

Health check: `https://campusconnect-1-l4h2.onrender.com/api/health`

## 2. Frontend: Render Static Site

In Render: **New → Static Site → same GitHub repository**.

| Setting | Value |
| :--- | :--- |
| Branch | `main` |
| Root Directory | `frontend` |
| Build Command | `npm install && npm run build` |
| Publish Directory | `dist` |

Add **frontend environment variable**:

| Key | Value |
| :--- | :--- |
| `VITE_API_URL` | `https://campusconnect-1-l4h2.onrender.com` |

The accompanying upgrade to `frontend/src/main.jsx` reads `VITE_API_URL` at build time. Without that change, the original `fetch('/api' + path)` requests target the frontend domain instead of the separate API service.

Select **Save, rebuild and deploy** for the frontend after changing its environment variables. Vite embeds `VITE_*` values in the compiled JS bundle; they must not contain secrets.

## 3. Verify

1. Open backend `/api/health`. Expected `{"status":"ok"}`.
2. Open frontend https://campusconnect-web-mvbs.onrender.com/ .
3. Confirm six example courses appear (if the original seed data is unchanged).
4. Open browser developer tools → Network and confirm requests reach `https://campusconnect-1-l4h2.onrender.com/api/courses`.
5. Test demo signup, enrollment, and bookmark, using a unique test password. Do not enter sensitive real-world data.
6. Confirm GitHub Actions workflow succeeds after your commit.

## Troubleshooting

| Symptom | Most likely cause | What to check |
| :--- | :--- | :--- |
| Website opens but courses are blank | API origin not configured | `VITE_API_URL` and frontend rebuild |
| CORS error in browser | Wrong allowed origin | Backend `CORS_ORIGINS` must exactly match frontend HTTPS origin, no trailing slash |
| Auth works then account disappears | Ephemeral SQLite | Set up persistent PostgreSQL and migrations |
| 502 / start failure | Build or startup error | Render Web Service Logs, Python installation and start command |
| Changes missing after GitHub push | Old deployment | Render latest deployment status and rebuild |

**Security first:** set a real `SECRET_KEY` on your deployed backend, limit public-data collection, and implement production security safeguards before onboarding actual students.
