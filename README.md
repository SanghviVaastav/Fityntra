# FITYNTRA — Adaptive AI/ML-Driven Fitness and Nutrition Platform with Injury-Aware Wellness Support

> An intelligent, culturally aware, and clinically safe AI-powered wellness ecosystem that combines Machine Learning, Nutrition Intelligence, and Injury-Aware Rehabilitation Assistance. 

---

## Overview

FITYNTRA is an advanced AI/ML-based fitness and nutrition platform designed to deliver personalized wellness recommendations while maintaining strict clinical safety standards. Unlike conventional fitness applications that rely on static calorie formulas and generic workout plans, FITYNTRA integrates Machine Learning models, localized Indian nutritional datasets, and injury-aware rehabilitation intelligence to create adaptive and safe recommendations for users. 

The platform combines:

* Personalized calorie and nutrition prediction
* Injury-aware exercise recommendations
* AI-powered rehabilitation coaching
* Indian diet optimization
* Multi-agent AI architecture
* Secure production-ready backend APIs

---

# Key Features

## Personalized Nutrition Recommendation

* AI-driven calorie target prediction
* Protein density optimization
* Indian meal plan generation
* Vegetarian/Vegan-aware filtering
* Allergen-aware recommendation engine
* Macro balancing using ML models

## Injury-Aware Rehabilitation Coach (“Reha”)

* Natural language injury analysis
* Pain severity classification
* Safe rehabilitation guidance
* Contraindicated exercise filtering
* Deterministic safety rules
* Hard-stop alerts for severe injuries

## Machine Learning Intelligence

* XGBoost-powered prediction models
* Calorie burn estimation
* Nutrition scoring engine
* Regression-based optimization pipeline
* Data leakage prevention architecture

## Multi-Agent AI Architecture

* ML classifier as mathematical guardrail
* LLM-assisted conversational interface
* Retrieval-based deterministic recommendations
* SQL-powered safety filtering

## Full Stack Deployment

* React frontend
* FastAPI backend
* JWT authentication
* PostgreSQL/Supabase integration
* Real-time inference APIs
* Cloud deployment ready

---

# Problem Statement

Most existing fitness applications suffer from several critical limitations:

* Static BMR-based calculations
* Lack of personalization
* Western-centric diet datasets
* Unsafe workout recommendations
* No injury-awareness mechanisms
* Generic chatbot hallucinations
* Poor clinical safety standards

FITYNTRA addresses these limitations by integrating Machine Learning, NLP, and deterministic clinical safety guardrails into a unified wellness platform. 

---

# Objectives

The major objectives of the project include:

* Building a robust AI-driven fitness ecosystem
* Developing XGBoost-based predictive models
* Creating injury-aware rehabilitation intelligence
* Engineering Indian diet-aware recommendation systems
* Deploying secure production-grade APIs
* Integrating conversational AI with deterministic clinical rules



---

# System Architecture

```text
┌────────────────────┐
│    React Frontend  │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│   FastAPI Backend  │
│ Authentication API │
│ Recommendation API │
│ Rehab Coach API    │
└─────────┬──────────┘
          │
 ┌────────┴────────┐
 ▼                 ▼
ML Service Layer   PostgreSQL/Supabase
(XGBoost Models)   Database
          │
          ▼
 Multi-Agent NLP Pipeline
          │
          ▼
 Claude / Gemini LLM
```

---

# Tech Stack

## Frontend

* React.js
* Vite
* HTML5
* CSS3

## Backend

* FastAPI
* SQLAlchemy
* Pydantic
* Passlib (bcrypt)
* JWT Authentication

## Machine Learning

* Python
* Scikit-Learn
* XGBoost
* Pandas
* NumPy

## Database

* SQLite (Development)
* Supabase PostgreSQL (Production)

## NLP & AI

* Anthropic Claude 3.5 Sonnet
* Google Gemini API



---

# Machine Learning Pipeline

## 1. Data Collection

Datasets used:

* ICMR-NIN Indian Nutrition Dataset
* Physiopedia rehabilitation protocols
* Synthetic biometric datasets

## 2. Data Engineering

* Missing value imputation
* Feature normalization
* Regex-based clinical keyword extraction
* Macro-ratio feature engineering

## 3. Model Development

Models developed for:

* Calorie prediction
* Calorie burn estimation
* Protein density scoring
* Severity classification

## 4. Model Optimization

* Baseline Random Forest implementation
* Migration to XGBoost
* Hyperparameter tuning
* Regression strategy optimization

## 5. Model Deployment

* Pickle serialization (.pkl)
* Lazy loading in FastAPI
* Real-time API inference



---

# Multi-Agent Rehab Coach (“Reha”)

The rehabilitation assistant follows a clinically safe multi-stage architecture:

## Workflow

1. User describes injury in natural language
2. NLP extracts symptoms and injury parameters
3. XGBoost severity classifier evaluates injury
4. SQL avoid-list filters unsafe exercises
5. LLM formats safe rehabilitation guidance
6. Severe injuries trigger medical escalation

## Safety Guardrails

* No hallucinated exercises
* Deterministic rehabilitation database
* Contraindicated movement filtering
* Pain threshold analysis
* Medical escalation logic

This architecture ensures the AI does not generate unsafe rehabilitation suggestions. 

---

# Novelty of the Project

FITYNTRA introduces several innovative concepts:

## 1. Multi-Agent RAG-Based Fitness Intelligence

Instead of relying purely on LLM-generated outputs, the platform integrates:

* ML prediction engines
* SQL safety filters
* Deterministic rehabilitation rules

## 2. Injury-Aware AI Recommendations

Unlike traditional fitness bots, FITYNTRA:

* Detects injury severity
* Blocks unsafe exercises
* Recommends clinically safer alternatives

## 3. Indian Diet Optimization

The system supports:

* Regional Indian diets
* Vegetarian constraints
* Vegan filtering
* Cultural dietary boundaries

## 4. Filter-and-Rank Dietary Engine

A two-stage recommendation system:

1. SQL rule filtering
2. ML-based nutritional optimization



---

# Expected Outcomes

* High-accuracy calorie prediction models
* Personalized Indian diet generation
* Automated injury triaging
* Secure scalable backend APIs
* Real-time AI-assisted wellness support
* Clinically safer rehabilitation workflows

Expected caloric prediction MAE:

* ~63.10 using XGBoost regression



---

# Security Features

* JWT-based authentication
* Password hashing using bcrypt
* Protected API endpoints
* Input validation using Pydantic
* Role-based architecture compatibility

---

# Project Workflow

```text
User Input
    ↓
Frontend Interface
    ↓
FastAPI API Layer
    ↓
ML/NLP Processing
    ↓
XGBoost Predictions
    ↓
Safety Filtering
    ↓
LLM Formatting
    ↓
Personalized Recommendation
```

---

# Installation Guide

## Clone Repository

```bash
git clone https://github.com/your-username/fityntra.git
cd fityntra
```

## Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run Backend

```bash
uvicorn app.main:app --reload
```

Backend runs on:

```text
http://127.0.0.1:8000
```

---

# Run Frontend

```bash
npm install
npm run dev
```

Frontend runs on:

```text
http://localhost:5173
```

---

# API Modules

## Authentication APIs

* Register user
* Login user
* JWT token generation

## Nutrition APIs

* Calorie prediction
* Protein optimization
* Diet recommendation

## Rehabilitation APIs

* Injury assessment
* Exercise safety filtering
* Rehab plan generation

## ML Inference APIs

* Calorie burn prediction
* Severity classification
* Personalized scoring

---

# Future Enhancements

* Wearable device integration
* Real-time heart-rate analytics
* Computer vision-based posture correction
* Voice-enabled AI coach
* Mobile application deployment
* Advanced reinforcement learning recommendations
* Personalized supplement intelligence

---

# Research Contributions

The project contributes to:

* AI in healthcare
* Injury-aware fitness intelligence
* Personalized nutrition systems
* Clinical AI safety mechanisms
* Indian diet recommendation systems

---

# Team

## COHORT 23

* Vrushank Skanda B
* Sadiya Kulsum
* Ravi
* Mohammed Issa Ilyas
* Sruthi K S
* Rafa Rahmath
* Saayanth M
* Vaastav L Sanghvi
* Prokshith Jain
* Avinash Nashi




---

# References

The project is based on extensive research in:

* AI-driven fitness recommendation systems
* Personalized nutrition intelligence
* Rehabilitation-aware machine learning
* Indian diet analysis
* NLP-based healthcare assistants

Key references include:

* Scientific Reports
* IJARCCE
* IRJAEM
* Healthcare Journal
* Electronics Journal
* ResearchGate publications



---

# License

This project is developed for academic and research purposes.

---

# Acknowledgement

We sincerely acknowledge all faculty mentors, contributors, open-source communities, and research resources that supported the successful development of FITYNTRA.

---

# Disclaimer

FITYNTRA is an AI-assisted wellness platform and should not replace professional medical consultation. Users with severe injuries or medical conditions should consult certified healthcare professionals before following any rehabilitation or fitness program.

---
:
