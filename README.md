# 🎤 The Debate™ — Trump vs. Busey

> *Two minds. Zero consensus. Infinite confusion.*

An AI-powered debate app where satirical versions of Donald Trump and Gary Busey argue about **any topic you choose** — or any file you upload. Built entirely on the free tier.

---

## Stack (100% Free)

| Layer | Tool | Cost |
|---|---|---|
| AI Backend | Groq API — Llama 3.3 70B | Free tier |
| API Server | FastAPI + Uvicorn | Free / open source |
| Frontend | Vanilla HTML/CSS/JS | Free |
| Backend Hosting | Render.com | Free tier |
| Frontend Hosting | Vercel or Netlify | Free tier |

---

## Project Structure

```
the-debate/
├── backend/
│   ├── main.py            ← FastAPI app + debate engine
│   ├── requirements.txt   ← Python dependencies
│   └── .env.example       ← Copy to .env and add your key
└── frontend/
    └── index.html         ← Entire frontend (single file, no build)
```

---

## Setup

### 1. Get a Free Groq API Key
Sign up at **https://console.groq.com** — free tier gives you 6,000 tokens/minute on Llama 3.3 70B.
Each debate uses ~800–1,200 tokens = ~5 debates per minute on the free tier.

### 2. Backend

```bash
cd backend
pip install -r requirements.txt

cp .env.example .env
# Edit .env: GROQ_API_KEY=your_key_here

uvicorn main:app --reload
# → running at http://localhost:8000
```

### 3. Frontend

```bash
# Just open it — no build step needed
open frontend/index.html
```

---

## Deployment (Free)

### Backend → Render.com
1. Push this repo to GitHub
2. New Web Service → connect repo → Root Directory: `backend`
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add env var: `GROQ_API_KEY`
6. Deploy → get your free URL

### Frontend → Vercel or Netlify
1. Update `API_URL` in `frontend/index.html` with your Render URL
2. Drag the `frontend/` folder into vercel.com or app.netlify.com/drop

Total cost: **$0.**

---

## Features

- 🎤 **Text topic** — type anything and watch the chaos unfold
- 📄 **File upload** — upload `.txt` or `.pdf` and they argue about its contents
- 🔁 **Adjustable rounds** — 2 to 5 rounds of back-and-forth
- 🗾 **Vote on the winner** — with in-character victory lines
- 📋 **Copy to clipboard** — share the debate anywhere

---

## Disclaimer

This app is satire and parody for entertainment purposes only. All AI-generated content is entirely fictional. No actual positions, statements, or beliefs of any real individuals are represented. This is a comedy application in the tradition of SNL, parody accounts, and late night satire.

---

*Built with chaos and love by Or4cl3 AI Solutions*  
*ANAL Module not included (that’s a different product)*
