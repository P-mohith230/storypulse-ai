from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import init_db
from app.api.routes import health
from app.api.api_v1 import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Interactive cinematic mobile storytelling platform integrated with Gnani AI voice intelligence.",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS setup for mobile and web testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup events
@app.on_event("startup")
def on_startup():
    init_db()
    print("[StoryPulse AI] Database initialized & Story Engine ready.")

# Include routers
app.include_router(health.router, tags=["System Health"])
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
