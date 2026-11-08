# StoryPulse AI — Deployment & Setup Guide
**Document ID:** `15_DEPLOYMENT_GUIDE`  
**Version:** `1.0.0`  
**Status:** Approved  
**Last Updated:** 2026-11-08  

---

## 1. Prerequisites
- **Node.js:** v18+ (Verified with v22.16.0)
- **Python:** v3.11+ (Verified with v3.13.5)
- **Git:** 2.40+
- **Expo CLI / EAS CLI:** Installed globally or via `npx`
- **Android Device or Emulator:** For native testing

---

## 2. Backend Setup & Local Running

```bash
# 1. Navigate to backend directory
cd backend

# 2. Create virtual environment (optional but recommended)
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
copy .env.example .env
# Edit .env and supply GNANI_API_KEY if available.

# 5. Run FastAPI development server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The interactive OpenAPI docs are immediately accessible at `http://localhost:8000/docs`.

---

## 3. Mobile Client Setup & Android Execution

```bash
# 1. Navigate to mobile directory
cd mobile

# 2. Install NPM dependencies
npm install

# 3. Configure API URL in .env
# For Android Emulator: http://10.0.2.2:8000
# For Physical Device: http://<YOUR_LOCAL_IP>:8000
echo "EXPO_PUBLIC_API_URL=http://10.0.2.2:8000" > .env

# 4. Start Expo development server
npx expo start
```

Press `a` in the terminal to launch on a running Android emulator or scan the QR code with the **Expo Go** app on a physical Android phone.

---

## 4. Production Deployment Configurations

### 4.1 Backend (Render / Railway / AWS EC2)
- Dockerfile provided in `backend/Dockerfile`.
- Port: `8000`.
- Environment Variables:
  - `DATABASE_URL`: Cloud PostgreSQL connection string (or persistent SQLite volume).
  - `GNANI_API_KEY`: Production Gnani Vachana key.
  - `CORS_ORIGINS`: Allowed client origins.

### 4.2 Mobile APK Build (Android Standalone)
```bash
# Build standalone Android APK with Expo EAS
npx eas build -p android --profile preview
```

