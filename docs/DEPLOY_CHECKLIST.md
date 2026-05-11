# Deploy Checklist — Fityntra v1.0
**Date:** 2026-05-02 | **Stack:** React/Vite → Netlify · FastAPI/Python → Render · Supabase PostgreSQL

---

## ⚠️ Blockers — fix these before anything else

- [ ] **ML models not in git** — `.gitignore` had `*.pkl` blocking all models. Already fixed in this session. Verify by running `git status` in the backend folder — `app/ml_models/*.pkl` must appear as untracked/new files.
- [ ] **79 MB RF model** — `fitendra_rf_model.pkl` (79 MB, used for fitness level prediction) needs Git LFS before pushing:
  ```bash
  git lfs install
  git lfs track "app/ml_models/fitendra_rf_model.pkl"
  git add .gitattributes
  git add app/ml_models/
  git commit -m "feat: add production ML models"
  git push
  ```
- [ ] **SECRET_KEY is a placeholder** — the current value is `your-super-secret-key-change-in-production`. Use this generated key in Render's env vars (do NOT commit it):
  ```
  31416d6bcf764255863587c2107761faf8003e8da751996c32911ef7a0881e27
  ```
- [ ] **CORS_ORIGINS must include Netlify URL** — deploy Render first, then update `CORS_ORIGINS` in Render env vars to your Netlify domain before testing.

---

## Phase 1 — Backend on Render

### 1.1 Repo setup
- [ ] Push backend folder to GitHub (or connect existing repo)
- [ ] Confirm `app/ml_models/` shows all 7 `.pkl` files in the commit
- [ ] Confirm `render.yaml` is present at repo root
- [ ] Confirm `.env` is in `.gitignore` (secrets never committed)

### 1.2 Create Render service
- [ ] Go to [render.com](https://render.com) → New → Web Service
- [ ] Connect GitHub repo, select the backend folder as root directory
- [ ] Render auto-detects `render.yaml` — verify:
  - Build command: `pip install -r requirements.txt`
  - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
  - Runtime: Python 3.11

### 1.3 Set environment variables in Render dashboard
| Variable | Value |
|----------|-------|
| `DATABASE_URL` | `postgresql://postgres:Vrushank%402026@db.uubvnzpzubbrvbwtwkbs.supabase.co:5432/postgres` |
| `SECRET_KEY` | `31416d6bcf764255863587c2107761faf8003e8da751996c32911ef7a0881e27` |
| `GROQ_API_KEY` | *(from your local .env)* |
| `GROQ_MODEL` | `llama-3.3-70b-versatile` |
| `CORS_ORIGINS` | `["https://<your-site>.netlify.app"]` *(add after Netlify deploy)* |
| `DEBUG` | `False` |
| `ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` |
| `MAX_HISTORY_TURNS` | `20` |

### 1.4 Verify Render deploy
- [ ] Build succeeds — no pip install errors
- [ ] Startup log shows `Application startup complete.`
- [ ] Startup log shows `Database tables created / verified` (Supabase connected)
- [ ] Startup log shows all 3 XGBoost models loading (calorie, nutrition, exercise)
- [ ] Note your Render URL: `https://fityntra-backend.onrender.com` (or similar)
- [ ] Hit `https://<render-url>/health` — expect `{"status":"ok",...}`

---

## Phase 2 — Frontend on Netlify

### 2.1 Configure environment variable
- [ ] In Netlify dashboard → Site settings → Environment variables, add:
  ```
  VITE_API_URL = https://<your-render-url>.onrender.com
  ```
  *(Do NOT use localhost — this variable is baked into the build)*

### 2.2 Create Netlify site
- [ ] Go to [netlify.com](https://netlify.com) → Add new site → Import from Git
- [ ] Connect GitHub repo, set **base directory** to `frontend`
- [ ] Netlify auto-detects `netlify.toml` — verify:
  - Build command: `npm run build`
  - Publish directory: `dist`
  - Node version: 20
- [ ] Deploy

### 2.3 Verify Netlify deploy
- [ ] Build succeeds — no Vite/React errors
- [ ] Open Netlify URL — login screen loads
- [ ] Open browser DevTools → Network → confirm API calls go to Render URL (not localhost)
- [ ] Navigate directly to `https://<netlify-url>/reha` — confirm it does NOT return 404 (SPA routing working)

---

## Phase 3 — Update CORS and end-to-end smoke test

### 3.1 Update CORS
- [ ] In Render dashboard, update `CORS_ORIGINS` to the real Netlify URL:
  ```
  ["https://<your-site>.netlify.app"]
  ```
- [ ] Trigger a Render redeploy (Manual Deploy → Deploy latest commit)

### 3.2 Smoke test — run these in order
- [ ] **Signup** — create a new account on the live site
- [ ] **Login** — log in with that account
- [ ] **Dashboard** — streak loads (shows `0 Days`, not `…`)
- [ ] **REHA coach** — send a message, confirm green "Connected to Groq AI" status and real AI reply
- [ ] **Health calc** — calculate BMI/TDEE, confirm ML fitness level badge appears
- [ ] **Diet AI Plan** — generate plan, confirm XGBoost calorie prediction returns
- [ ] **Workout AI Plan** — generate plan, confirm weekly schedule appears
- [ ] **Macro tracker** — log a food item, check Supabase `food_logs` table for the entry
- [ ] **Token expiry** — wait 30 min (or manually expire token), confirm app auto-redirects to login

### 3.3 Check Supabase
- [ ] Open Supabase → Table Editor → `users` — confirm signup created a row
- [ ] Open `food_logs` — confirm macro tracker entries are persisting
- [ ] Open `prediction_logs` — confirm diet/workout predictions are being audited
- [ ] Supabase project is NOT paused (free tier auto-pauses after ~1 week — enable "never pause" in project settings if available)

---

## Post-deploy

- [ ] Update `VITE_API_URL` in `.env` back to `http://127.0.0.1:8000` for local dev (production value lives in Netlify only)
- [ ] Share the Netlify URL with testers
- [ ] Monitor Render logs for the first 30 minutes (`Logs` tab in Render dashboard)
- [ ] Monitor Supabase for unexpected growth in `prediction_logs`

---

## Rollback plan

| Layer | How to rollback |
|-------|----------------|
| **Frontend** | Netlify dashboard → Deploys → click any previous deploy → "Publish deploy" — instant |
| **Backend** | Render dashboard → Manual Deploy → select previous commit SHA — ~2 min |
| **Database** | Supabase → No rollback needed for schema (tables are additive). For data issues, use Supabase SQL editor to query/fix rows. |

### Rollback triggers
- Error rate in Render logs exceeds 5% of requests
- Any prediction endpoint consistently returns 500
- Groq API returns errors (check `GROQ_API_KEY` validity at [console.groq.com](https://console.groq.com))
- Supabase DNS error on startup (project paused — restore at supabase.com)
- Login returns 401 for valid credentials (SECRET_KEY mismatch between local and Render)

---

## Known limitations at launch (not blockers)

- JWT session expires after 30 min — user must re-login (no refresh token yet)
- Dashboard meal log is still mock data — not persisted to backend
- Progress page weight chart is static
- Community page has no backend
- REHA chat history is in-memory only — resets on Render restart (free tier sleeps after inactivity)
