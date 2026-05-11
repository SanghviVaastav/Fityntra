# Fityntra — Project Memory

## Overview
**Fityntra** is a fitness/wellness web app built with **React + Vite** (frontend) and **FastAPI + Python** (backend).

---

## Project Structure (after reorganisation — May 2026)

```
Fityntra/
├── frontend/          ← React + Vite app (was frontend/)
├── backend/           ← FastAPI + Python (was "backend")
├── docs/              ← DEPLOY_CHECKLIST.md, memory.md
└── tests/             ← test_fityntra.py
```

### Frontend
- **Path:** `C:\Users\sejal\OneDrive\Desktop\Fityntra\frontend`
- **Stack:** React + Vite
- **Run:**
  ```powershell
  cd C:\Users\sejal\OneDrive\Desktop\Fityntra\frontend
  npm.cmd install
  npm.cmd run dev
  ```
- **URL:** `http://localhost:5173`

### Backend
- **Path:** `C:\Users\sejal\OneDrive\Desktop\Fityntra\backend`
- **Stack:** Python + FastAPI + Supabase PostgreSQL + XGBoost + Random Forest + Groq LLM
- **Run:**
  ```powershell
  cd C:\Users\sejal\OneDrive\Desktop\Fityntra\backend
  uvicorn app.main:app --reload
  ```
- **URL:** `http://127.0.0.1:8000`
- **Swagger UI:** `http://127.0.0.1:8000/docs`

---

## Frontend Pages
- Login screen (real JWT auth)
- Dashboard (real streak from backend)
- Health Calculator (ML fitness level prediction)
- Diet Recommender (hardcoded + AI Plan tab → XGBoost)
- Workout Recommender (hardcoded + AI Plan tab → backend)
- REHA Rehab Coach (real Groq AI, offline fallback)
- Macro Tracker (logs to backend silently)
- Progress Page
- Community Page (static)
- Settings Page

---

## Backend — Full API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Server health check |
| POST | `/auth/login` | JWT login (bcrypt + python-jose) |
| POST | `/users/` | Register a new user |
| GET | `/users/{user_id}` | Get user profile (auth required) |
| PUT | `/users/{user_id}` | Update user profile (auth required) |
| POST | `/predict/diet` | XGBoost calorie target + Indian meal plan |
| POST | `/predict/workout` | Personalised weekly workout plan |
| POST | `/predict/nutrition-score` | XGBoost Indian food protein density score |
| POST | `/predict/exercise-burn` | XGBoost exercise calorie burn estimator |
| POST | `/predict/injury-chat` | NLP keyword-based injury rehab chatbot |
| POST | `/predict/fitness-level` | Random Forest fitness level classifier |
| POST | `/log/food` | Log a meal with macros |
| GET | `/streak/{user_id}` | Get user streak & activity stats |
| POST | `/rehab/chat` | REHA Coach — Groq LLM with clinical guardrails |
| POST | `/rehab/reset` | Reset a REHA chat session |

---

## Database: Supabase PostgreSQL ✅
- **URL:** `db.uubvnzpzubbrvbwtwkbs.supabase.co`
- Switched from SQLite to Supabase in May 2026
- Tables: `users`, `food_logs`, `workout_logs`, `streaks`, `prediction_logs`
- `DATABASE_URL` is set in backend `.env`

---

## Backend Environment (`.env`)
```
DATABASE_URL=postgresql://postgres:...@db.uubvnzpzubbrvbwtwkbs.supabase.co:5432/postgres
GROQ_API_KEY=<set>
GROQ_MODEL=llama-3.3-70b-versatile
MAX_HISTORY_TURNS=20
SECRET_KEY=31416d6bcf764255863587c2107761faf8003e8da751996c32911ef7a0881e27
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=["http://localhost:5173"]
DEBUG=True
```

---

## Integration Status (May 2026)

| Component | Status | Notes |
|-----------|--------|-------|
| **Login/Signup** | ✅ | `POST /users/` + `POST /auth/login`, JWT decoded, full profile stored |
| **REHA Coach** | ✅ | `POST /rehab/chat`, session_id persisted, offline fallback |
| **Diet Recommender** | ✅ | AI Plan tab → `POST /predict/diet` (XGBoost) |
| **Workout Recommender** | ✅ | AI Plan tab → `POST /predict/workout` |
| **Dashboard streak** | ✅ | `GET /streak/{user_id}` on mount |
| **MacroTracker** | ✅ | Silent `POST /log/food` on each entry |
| **HealthCalc** | ✅ | `POST /predict/fitness-level` (Random Forest) after BMI calc |
| **Token expiry** | ✅ | Auto-logout on 401 via `auth:expired` custom event |
| **User profile security** | ✅ | GET/PUT /users now require JWT auth |
| **Dashboard macros** | 🟡 Mock | Meals still hardcoded, editable locally |
| **ProgressPage** | 🟡 Mock | Weight chart static; achievements use localStorage |
| **CommunityPage** | 🟡 Static | No backend planned |

---

## Key Files (frontend)
- `src/api/fityntra.js` — centralized API client, enum mappers, JWT decoder
- `src/pages/LoginPage.jsx` — real auth, expanded signup, in-app success message
- `src/App.jsx` — user prop threading, auto-logout on token expiry
- `src/components/RehaCoach.jsx` — Groq AI + offline fallback + session reset
- `src/components/DietRecommender.jsx` — 🤖 AI Plan tab (XGBoost)
- `src/components/WorkoutRecommender.jsx` — 🤖 AI Plan tab + injury mods
- `src/components/Dashboard.jsx` — real streak, AbortController cleanup
- `src/components/MacroTracker.jsx` — silent food log to backend
- `src/components/Healthcalc.jsx` — ML fitness level badge
- `src/pages/ProgressPage.jsx` — fixed earnedCount bug, removed dead component

---

## Key Files (backend)
- `app/routers/users.py` — GET/PUT endpoints secured with JWT auth
- `app/schemas.py` — UserUpdate moved here from router
- `app/services/rehab_service.py` — Groq LLM, red-flag guardrails, contraindications
- `app/services/ml_service.py` — loads 4 production models at startup
- `render.yaml` — Render deployment config

---

## ML Models in Production (`backend/app/ml_models/`)
| File | Size | Used for |
|------|------|---------|
| `fitendra_rf_model.pkl` | 79 MB | Fitness level prediction (Random Forest) |
| `calorie_xgb.pkl` | 1.4 MB | Daily calorie target (XGBoost) |
| `exercise_xgb.pkl` | 868 KB | Exercise calorie burn (XGBoost) |
| `nutrition_xgb.pkl` | 832 KB | Food protein density score (XGBoost) |
| `calorie_features.pkl` | — | Feature list for calorie model |
| `exercise_features.pkl` | 4 KB | Feature list for exercise model |
| `nutrition_features.pkl` | — | Feature list for nutrition model |

---

## Deployment Plan (Netlify + Render)
- Frontend → Netlify (base dir: `frontend/`, build: `npm run build`, publish: `dist`)
- Backend → Render (start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`)
- Set `VITE_API_URL` in Netlify env to Render URL
- Set `CORS_ORIGINS` in Render env to Netlify URL
- See `docs/DEPLOY_CHECKLIST.md` for full step-by-step

---

## Bugs Fixed (May 2026)
1. `App.jsx` default route passed `userName` instead of `user` to Dashboard
2. `GET /users/{id}` and `PUT /users/{id}` had no auth — anyone could read/edit any profile
3. JWT decode failure → `userId=undefined` → downstream crashes (now throws clear error)
4. `BASE_URL` hardcoded → now reads `VITE_API_URL` env var
5. No token expiry handling → now auto-logout on 401
6. `MacroTracker` qty_grams calculation always returned `qty*100` (tautological math)
7. `alert()` on signup → replaced with inline green success message
8. Password not cleared after signup
9. `Dashboard useEffect` had no cleanup → state update on unmounted component
10. `ProgressPage` earnedCount counted stale localStorage keys → wrong X/8 display
11. Dead `AchievementsPanel` component in ProgressPage (defined but never rendered)
12. `UserUpdate` schema defined inline in router → moved to `schemas.py`
13. `main.py` CORS hardcoded to localhost — now reads `CORS_ORIGINS` from `.env` via `settings.cors_origins`
14. Duplicate `CORSMiddleware` import in `main.py` — removed
15. Stale FastAPI Swagger description ("JWT auth upcoming") — updated to reflect live state
16. `UserUpdate` appended at bottom of `schemas.py` after REHA schemas — moved to after `UserResponse`
17. `rehaChat` sent no auth token — now accepts optional `token` param; `user?.token` passed from `RehaCoach.jsx`
18. `predictFitnessLevel` sent no auth token — same fix; `user?.token` passed from `Healthcalc.jsx`

---

## Current Folder Structure
```
Fityntra/
├── backend/           ← FastAPI backend (rebuilt from "Only backend" zip + all changes applied)
├── frontend/          ← React + Vite frontend (was fityntra-app)
├── docs/              ← memory.md, DEPLOY_CHECKLIST.md
├── tests/             ← test_fityntra.py
└── Only backend/      ← original zip/folder (source of truth for recovery)
```

> ⚠️ `Only backend/` should be kept until the first successful production deploy as a safety backup.
