import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from app.core.config import settings
from app.core.database import init_db
from app.api.routes import health
from app.api.api_v1 import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Interactive cinematic mobile & web storytelling platform integrated with Gnani AI voice intelligence.",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Security and cache-control middleware
@app.middleware("http")
async def add_security_and_cache_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    if request.url.path.startswith("/static/images/"):
        response.headers["Cache-Control"] = "public, max-age=86400, immutable"
    return response

# CORS setup for mobile and web testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths for static web files and assets
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Startup events
@app.on_event("startup")
def on_startup():
    init_db()
    print("[StoryPulse AI] Database initialized & Story Engine ready.")

# Serve responsive web application
@app.get("/", include_in_schema=False)
def serve_spa():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "StoryPulse AI API is live. Static UI build not found."}

# Mount static assets (images, css, js, audio)
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Include routers
app.include_router(health.router, tags=["System Health"])
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)


