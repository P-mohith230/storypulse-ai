# StoryPulse AI — Vercel Serverless Deployment Guide
**Document ID:** `17_VERCEL_DEPLOYMENT_GUIDE`  
**Version:** `1.0.0`  
**Target Environment:** Vercel Serverless Python Runtime (`@vercel/python`)  
**Last Updated:** 2026-11-10  

---

## 1. Overview

StoryPulse AI is configured for one-click deployment to **Vercel** using `@vercel/python` serverless runtime and static edge caching.

The deployment bundles:
1. **FastAPI Backend (`/api/index.py` & `/backend`):** Serverless ASGI execution handling sessions, deterministic narrative branching, and Gnani AI voice orchestration.
2. **Responsive Mobile-First Web Application (`/backend/app/static`):** Served directly with client-side Web Audio, MediaRecorder voice capture, and PWA service worker caching.

---

## 2. Architecture & File Configuration

### 2.1 Routing Matrix (`vercel.json`)
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ]
}
```

### 2.2 Serverless Storage Strategy
- On Vercel, the root filesystem is read-only. StoryPulse automatically switches its SQLite database path to `/tmp/storypulse.db` and audio cache to `/tmp/audio_cache/`.
- For multi-region persistent cross-session storage in production, provide a PostgreSQL connection URL via the `DATABASE_URL` environment variable.

---

## 3. Step-by-Step Vercel Deployment

### Method A: Deploy via Vercel Web Dashboard (Recommended)

1. Navigate to [https://vercel.com/new](https://vercel.com/new).
2. Connect your GitHub account and import `P-mohith230/storypulse-ai`.
3. In **Project Settings**:
   - **Framework Preset:** Other
   - **Root Directory:** `./`
4. Expand **Environment Variables** and add:
   - `GNANI_API_KEY`: `vach_1ytE2CY5X2P8KpL3...`
   - `GNANI_BASE_URL`: `https://api.vachana.ai`
   - `GNANI_PRISMA_ENDPOINT`: `/stt/v3`
   - `GNANI_TIMBRE_ENDPOINT`: `/api/v1/tts/inference`
   - `GNANI_MOCK_FALLBACK`: `True`
5. Click **Deploy**. Vercel will build the runtime and provide your live URL (e.g. `https://storypulse-ai.vercel.app`).

### Method B: Deploy via Vercel CLI

```bash
# 1. Install Vercel CLI
npm install -g vercel

# 2. Login to Vercel
vercel login

# 3. Deploy to production
vercel --prod
```

---

## 4. Verification Post-Deployment

After deployment finishes, verify the live endpoints:
- `GET https://your-project.vercel.app/` -> Renders StoryPulse Web App (HTTP 200)
- `GET https://your-project.vercel.app/health` -> Returns `{"status":"healthy","database":"connected"}`
- `GET https://your-project.vercel.app/api/v1/stories` -> Returns 5 story domains catalog
- `GET https://your-project.vercel.app/docs` -> OpenAPI Swagger documentation
