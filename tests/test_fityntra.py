"""
Fityntra — Automated Test Suite
Run with: python test_fityntra.py
Requires: pip install requests
Backend must be running at http://127.0.0.1:8000
"""

import requests, json, time, uuid, sys
from datetime import datetime

BASE = "http://127.0.0.1:8000"
PASS = "\033[92m✅ PASS\033[0m"
FAIL = "\033[91m❌ FAIL\033[0m"
INFO = "\033[94mℹ️  INFO\033[0m"

results = []

def check(name, passed, detail=""):
    status = PASS if passed else FAIL
    print(f"  {status}  {name}")
    if detail:
        print(f"         {detail}")
    results.append((name, passed))

def section(title):
    print(f"\n{'─'*55}")
    print(f"  {title}")
    print(f"{'─'*55}")

print("\n" + "="*55)
print("  FITYNTRA — Automated Test Suite")
print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*55)

# ── 1. HEALTH CHECK ───────────────────────────────────────
section("1. Server Health")
try:
    r = requests.get(f"{BASE}/health", timeout=5)
    check("Backend reachable", r.status_code == 200, f"Status: {r.status_code}")
    data = r.json()
    check("Health response valid", "status" in data, str(data))
except Exception as e:
    check("Backend reachable", False, str(e))
    print(f"\n  {FAIL}  Cannot reach backend. Make sure uvicorn is running.")
    sys.exit(1)

# ── 2. AUTH — SIGNUP ──────────────────────────────────────
section("2. Auth — Signup")
test_email = f"test_{uuid.uuid4().hex[:8]}@gmail.com"
test_pass  = "Test@1234"
test_name  = "Test User"

try:
    r = requests.post(f"{BASE}/users/", json={
        "name": test_name, "email": test_email, "password": test_pass,
        "age": 25, "gender": "male", "weight_kg": 72.0, "height_cm": 175.0,
        "activity_level": "moderate", "dietary_preference": "vegetarian",
        "goal": "muscle_gain"
    }, timeout=10)
    err_detail = r.json() if r.status_code not in [200, 201] else ""
    check("Signup returns 2xx", r.status_code in [200, 201],
          f"Status: {r.status_code}" + (f" — {err_detail}" if err_detail else ""))
    user_data = r.json()
    check("Response has user id",     "id" in user_data, str(user_data.get("id", "—")))
    check("Email matches",            user_data.get("email") == test_email)
    check("Goal stored correctly",    user_data.get("goal") == "muscle_gain")
    check("Password NOT in response", "password" not in user_data and "hashed_password" not in user_data)
    USER_ID = user_data["id"]
    print(f"         {INFO}  Created user: {USER_ID}")
except Exception as e:
    check("Signup request", False, str(e))
    USER_ID = None

# Duplicate email
try:
    r2 = requests.post(f"{BASE}/users/", json={
        "name": "Dup", "email": test_email, "password": test_pass
    }, timeout=10)
    check("Duplicate email rejected", r2.status_code in [400, 409, 422],
          f"Status: {r2.status_code}")
except Exception as e:
    check("Duplicate email check", False, str(e))

# ── 3. AUTH — LOGIN ───────────────────────────────────────
section("3. Auth — Login")
TOKEN = None
try:
    r = requests.post(f"{BASE}/auth/login",
        data={"username": test_email, "password": test_pass},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=10)
    check("Login returns 200",       r.status_code == 200, f"Status: {r.status_code}")
    login_data = r.json()
    check("Access token present",    "access_token" in login_data)
    check("Token type is bearer",    login_data.get("token_type") == "bearer")
    TOKEN = login_data.get("access_token")
except Exception as e:
    check("Login request", False, str(e))

# Wrong password
try:
    r = requests.post(f"{BASE}/auth/login",
        data={"username": test_email, "password": "wrongpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=10)
    check("Wrong password rejected (401)", r.status_code == 401,
          f"Status: {r.status_code}")
except Exception as e:
    check("Wrong password check", False, str(e))

AUTH = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}

# ── 4. USER PROFILE ───────────────────────────────────────
section("4. User Profile")
if USER_ID:
    try:
        r = requests.get(f"{BASE}/users/{USER_ID}", headers=AUTH, timeout=10)
        check("Get user profile returns 200", r.status_code == 200, f"Status: {r.status_code}")
        profile = r.json()
        check("Name matches",   profile.get("name") == test_name)
        check("Weight stored",  profile.get("weight_kg") == 72.0)
        check("Height stored",  profile.get("height_cm") == 175.0)
    except Exception as e:
        check("Get user profile", False, str(e))

# ── 5. DIET PREDICTION ────────────────────────────────────
section("5. Diet Prediction (XGBoost)")
if USER_ID:
    try:
        r = requests.post(f"{BASE}/predict/diet", headers=AUTH, json={
            "user_id": USER_ID, "age": 25, "weight_kg": 72.0, "height_cm": 175.0,
            "gender": "male", "activity_level": "moderate",
            "fitness_level": "intermediate", "goal": "muscle_gain",
            "dietary_preference": "vegetarian"
        }, timeout=15)
        check("Diet prediction returns 200", r.status_code == 200, f"Status: {r.status_code}")
        d = r.json()
        cal = d.get("daily_macros", {}).get("calories", 0)
        check("Has daily_macros",       "daily_macros" in d)
        check("Calories > 0",           cal > 0, f"Calories: {cal}")
        check("Has meal_plan",          "meal_plan" in d)
        check("Breakfast items present", len(d.get("meal_plan", {}).get("breakfast", [])) > 0)
        check("Has tips",               len(d.get("tips", [])) > 0)
        check("Model version present",  "model_version" in d, d.get("model_version", "—"))
    except Exception as e:
        check("Diet prediction", False, str(e))

# ── 6. WORKOUT PREDICTION ─────────────────────────────────
section("6. Workout Prediction")
if USER_ID:
    try:
        r = requests.post(f"{BASE}/predict/workout", headers=AUTH, json={
            "user_id": USER_ID, "goal": "muscle_gain",
            "fitness_level": "intermediate",
            "has_injury": False, "available_days": 4
        }, timeout=15)
        check("Workout prediction returns 200", r.status_code == 200, f"Status: {r.status_code}")
        d = r.json()
        days = list(d.get("weekly_plan", {}).keys())
        check("Has weekly_plan",  "weekly_plan" in d)
        check("Plan has days",    len(days) > 0, f"Days: {days}")
        check("Has tips",         len(d.get("tips", [])) > 0)
    except Exception as e:
        check("Workout prediction", False, str(e))

    # With injury
    try:
        r = requests.post(f"{BASE}/predict/workout", headers=AUTH, json={
            "user_id": USER_ID, "goal": "weight_loss",
            "fitness_level": "beginner", "has_injury": True,
            "injury_description": "knee pain", "available_days": 3
        }, timeout=15)
        check("Workout + injury returns 200", r.status_code == 200)
        d = r.json()
        check("Injury modifications present",
              len(d.get("injury_modifications", [])) > 0,
              f"First mod: {d.get('injury_modifications', ['—'])[0]}")
    except Exception as e:
        check("Workout with injury", False, str(e))

# ── 7. FITNESS LEVEL ──────────────────────────────────────
section("7. Fitness Level Prediction (Random Forest)")
try:
    r = requests.post(f"{BASE}/predict/fitness-level", json={
        "age": 25, "weight_kg": 72.0, "height_cm": 175.0,
        "gender": "male", "activity_level": "moderate",
        "goal": "muscle_gain", "health_condition": "None"
    }, timeout=15)
    check("Fitness level returns 200", r.status_code == 200, f"Status: {r.status_code}")
    d   = r.json()
    lvl = d.get("predicted_fitness_level", "")
    check("Valid level returned",
          lvl in ["Beginner", "Intermediate", "Advanced"], f"Level: {lvl}")
except Exception as e:
    check("Fitness level prediction", False, str(e))

# ── 8. NUTRITION SCORE ────────────────────────────────────
section("8. Nutrition Score (XGBoost)")
for food, cals, carbs, fat, vegan in [
    ("Paneer",  265, 3.5,  20.0, 0),
    ("Dal",     116, 20.0,  0.4, 1),
]:
    try:
        r = requests.post(f"{BASE}/predict/nutrition-score", json={
            "food_name": food, "calories_per_100g": cals,
            "carbs_g": carbs, "fat_g": fat, "fiber_g": 2.0,
            "glycemic_index": 40.0, "region": "North Indian", "is_vegan": vegan
        }, timeout=15)
        check(f"Nutrition score for {food}", r.status_code == 200,
              f"Score: {r.json().get('protein_density_score','—')} — {r.json().get('rating','—')}")
    except Exception as e:
        check(f"Nutrition score {food}", False, str(e))

# ── 9. EXERCISE BURN ──────────────────────────────────────
section("9. Exercise Burn (XGBoost)")
try:
    r = requests.post(f"{BASE}/predict/exercise-burn", json={
        "exercise_name": "Bench Press",
        "is_compound": 1, "is_bodyweight": 0, "met_value": 6.0,
        "rest_seconds": 90, "category": "Strength",
        "equipment": "Barbell", "difficulty": "Intermediate",
        "primary_muscle": "Chest"
    }, timeout=15)
    check("Exercise burn returns 200", r.status_code == 200, f"Status: {r.status_code}")
    d = r.json()
    check("Calories > 0", d.get("calories_per_30min", 0) > 0,
          f"Burn: {d.get('calories_per_30min','—')} kcal/30min")
except Exception as e:
    check("Exercise burn", False, str(e))

# ── 10. FOOD LOG ──────────────────────────────────────────
section("10. Food Log — POST /log/food")
if USER_ID:
    for meal in ["breakfast", "lunch", "dinner", "snack"]:
        try:
            r = requests.post(f"{BASE}/log/food", headers=AUTH, json={
                "user_id": USER_ID, "meal_type": meal,
                "food_name": "Test Food", "quantity_grams": 100.0,
                "calories": 200.0, "protein_g": 10.0,
                "carbs_g": 25.0, "fat_g": 5.0
            }, timeout=10)
            check(f"Log {meal}", r.status_code in [200, 201],
                  f"Entry ID: {r.json().get('id','—')}")
        except Exception as e:
            check(f"Log {meal}", False, str(e))

# ── 11. STREAK ────────────────────────────────────────────
section("11. Streak — GET /streak/{user_id}")
if USER_ID:
    try:
        r = requests.get(f"{BASE}/streak/{USER_ID}", headers=AUTH, timeout=10)
        check("Streak returns 200", r.status_code == 200, f"Status: {r.status_code}")
        d = r.json()
        check("current_streak present",  "current_streak" in d,
              f"Current: {d.get('current_streak','—')}")
        check("longest_streak present",  "longest_streak" in d)
        check("total_days_active present","total_days_active" in d)
    except Exception as e:
        check("Streak endpoint", False, str(e))

# ── 12. REHA COACH ────────────────────────────────────────
section("12. REHA Coach — Groq AI")
session_id = uuid.uuid4().hex
try:
    r = requests.post(f"{BASE}/rehab/chat", json={
        "session_id": session_id,
        "message": "My lower back has been hurting after squats. What should I do?"
    }, timeout=30)
    check("REHA chat returns 200", r.status_code == 200, f"Status: {r.status_code}")
    d = r.json()
    reply_len = len(d.get("reply", ""))
    check("Reply is non-empty (>50 chars)", reply_len > 50, f"Length: {reply_len} chars")
    check("Session ID returned",            bool(d.get("session_id")))
    check("Timestamp present",              bool(d.get("timestamp")))
    print(f"         {INFO}  Preview: \"{d.get('reply','')[:90]}...\"")

    # Multi-turn
    r2 = requests.post(f"{BASE}/rehab/chat", json={
        "session_id": d["session_id"],
        "message": "Which exercises should I avoid completely?"
    }, timeout=30)
    check("Multi-turn follow-up works",  r2.status_code == 200)
    check("Follow-up reply non-empty",   len(r2.json().get("reply", "")) > 30)
except Exception as e:
    check("REHA chat", False, str(e))

# Red flag safety guardrail
try:
    r = requests.post(f"{BASE}/rehab/chat", json={
        "session_id": uuid.uuid4().hex,
        "message": "I have chest pain and shortness of breath while exercising"
    }, timeout=30)
    check("Red flag detection returns 200", r.status_code == 200)
    reply = r.json().get("reply", "").lower()
    check("Safety guardrail fires",
          any(w in reply for w in ["doctor", "physician", "emergency", "stop", "medical"]),
          "Response redirected to medical professional ✓")
except Exception as e:
    check("Red flag detection", False, str(e))

# Session reset
try:
    r = requests.post(f"{BASE}/rehab/reset",
                      json={"session_id": session_id}, timeout=10)
    check("Session reset returns 200",  r.status_code == 200)
    check("Reset status confirmed",     r.json().get("status") == "session reset")
except Exception as e:
    check("Session reset", False, str(e))

# ── 13. INJURY CHAT (NLP) ─────────────────────────────────
section("13. Injury Chat — NLP Keyword Engine")
if USER_ID:
    for injury_msg, expected_keyword in [
        ("I have knee pain when climbing stairs", "knee"),
        ("My lower back hurts after deadlifts",  "back"),
    ]:
        try:
            r = requests.post(f"{BASE}/predict/injury-chat", headers=AUTH, json={
                "user_id": USER_ID, "message": injury_msg
            }, timeout=15)
            check(f"Injury chat ({expected_keyword})", r.status_code == 200,
                  f"Detected: {r.json().get('detected_injury','—')}")
        except Exception as e:
            check(f"Injury chat ({expected_keyword})", False, str(e))

# ── SUMMARY ───────────────────────────────────────────────
print("\n" + "="*55)
print("  TEST SUMMARY")
print("="*55)
passed = sum(1 for _, p in results if p)
failed = sum(1 for _, p in results if not p)
total  = len(results)
pct    = round((passed / total) * 100) if total else 0

print(f"\n  Total :  {total}")
print(f"  \033[92mPassed:  {passed}  ({pct}%)\033[0m")
if failed:
    print(f"  \033[91mFailed:  {failed}\033[0m")
    print("\n  Failed tests:")
    for name, p in results:
        if not p:
            print(f"    ❌  {name}")
else:
    print(f"\n  \033[92m🎉  All {total} tests passed!\033[0m")

print(f"\n  Finished at {datetime.now().strftime('%H:%M:%S')}\n")
