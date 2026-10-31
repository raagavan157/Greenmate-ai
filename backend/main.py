import os
import sys
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from config import settings
from database import db_manager
from utils.seed_data import seed_database
from routes import auth, plants, ai, garden, care, wishlist, guides, payments, admin

app = FastAPI(
    title="GreenMate AI - Intelligent Plant Care Platform",
    description="Full-stack AI-powered plant identification, disease diagnosis, and smart garden management platform.",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup Lifecycle
@app.on_event("startup")
def on_startup():
    try:
        db_manager.init_db()
        seed_database(db_manager)
    except Exception as e:
        print(f"Non-critical startup init warning: {e}")
    print("==================================================")
    print("GreenMate AI Backend Ready")
    print(f"Database Engine: {'MongoDB Atlas' if db_manager.is_atlas else 'Local Document Store (Resilient Mode)'}")
    print("==================================================")

# Include API Routers
app.include_router(auth.router)
app.include_router(plants.router)
app.include_router(ai.router)
app.include_router(garden.router)
app.include_router(care.router)
app.include_router(wishlist.router)
app.include_router(guides.router)
app.include_router(payments.router)
app.include_router(admin.router)

# Health & System Status Endpoint
@app.get("/api/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "app": "GreenMate AI",
        "database": {
            "mode": "MongoDB Atlas" if db_manager.is_atlas else "Local Document Store",
            "connected": True
        },
        "ai": {
            "provider": "Gemini API" if (settings.GEMINI_API_KEY and not settings.GEMINI_API_KEY.startswith("your_")) else "GreenMate Botanical Engine",
            "live_vision_ready": bool(settings.GEMINI_API_KEY and not settings.GEMINI_API_KEY.startswith("your_"))
        }
    }

# Mount uploads directory safely
uploads_dir = settings.ensure_upload_dir()
if uploads_dir.exists():
    app.mount("/uploads", StaticFiles(directory=str(uploads_dir)), name="uploads")

# Frontend directory
frontend_dir = backend_dir.parent / "frontend"
if not frontend_dir.exists():
    frontend_dir = backend_dir / "frontend"
if frontend_dir.exists():
    css_dir = frontend_dir / "css"
    if css_dir.exists():
        app.mount("/css", StaticFiles(directory=str(css_dir)), name="css")
    js_dir = frontend_dir / "js"
    if js_dir.exists():
        app.mount("/js", StaticFiles(directory=str(js_dir)), name="js")
    assets_dir = frontend_dir / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")

    def _serve_page(name: str):
        target = frontend_dir / f"{name}.html"
        if target.is_file() and target.exists():
            return FileResponse(target)
        index_file = frontend_dir / "index.html"
        if index_file.is_file() and index_file.exists():
            return FileResponse(index_file)
        return JSONResponse({
            "app": "GreenMate AI",
            "status": "online",
            "message": "Backend API Ready",
            "health": "/api/health"
        })

    # Serve HTML pages directly
    @app.get("/", tags=["Frontend"])
    @app.get("/index", tags=["Frontend"])
    @app.get("/index.html", tags=["Frontend"])
    def serve_home():
        return _serve_page("index")

    @app.get("/favicon.ico")
    def serve_favicon():
        fav = frontend_dir / "assets" / "favicon.ico"
        if fav.exists():
            return FileResponse(fav)
        return _serve_page("index")

    @app.get("/{page_name}.html", tags=["Frontend"])
    def serve_any_html(page_name: str):
        return _serve_page(page_name)

    @app.get("/explore", tags=["Frontend"])
    def serve_explore():
        return _serve_page("explore")

    @app.get("/plant-details", tags=["Frontend"])
    def serve_details():
        return _serve_page("plant-details")

    @app.get("/ai-doctor", tags=["Frontend"])
    def serve_ai_doctor():
        return _serve_page("ai-doctor")

    @app.get("/my-garden", tags=["Frontend"])
    def serve_garden():
        return _serve_page("my-garden")

    @app.get("/guides", tags=["Frontend"])
    def serve_guides():
        return _serve_page("guides")

    @app.get("/track-order", tags=["Frontend"])
    def serve_track_order():
        return _serve_page("track-order")

    @app.get("/admin", tags=["Frontend"])
    def serve_admin():
        return _serve_page("admin")

    @app.get("/login", tags=["Frontend"])
    def serve_login():
        return _serve_page("login")

    @app.get("/register", tags=["Frontend"])
    def serve_register():
        return _serve_page("register")

    @app.get("/profile", tags=["Frontend"])
    def serve_profile():
        return _serve_page("profile")

    # Comprehensive Wildcard SPA Route (prevents any frontend 404 Not Found error)
    @app.get("/{full_path:path}", tags=["Frontend"])
    def serve_wildcard_frontend(full_path: str):
        # Allow API endpoints to be treated normally
        if full_path.startswith("api/") or full_path == "api":
            return JSONResponse(status_code=404, content={"detail": "API endpoint not found"})
        
        # 1. Exact match in frontend (e.g. /favicon.ico, /robots.txt, etc.)
        direct_file = frontend_dir / full_path
        if direct_file.is_file() and direct_file.exists():
            return FileResponse(direct_file)

        # 2. Match with .html appended (e.g. /explore -> /explore.html)
        html_file = frontend_dir / f"{full_path}.html"
        if html_file.is_file() and html_file.exists():
            return FileResponse(html_file)

        # 3. Fallback to index.html
        if (frontend_dir / "index.html").exists():
            return FileResponse(frontend_dir / "index.html")
        return JSONResponse({"app": "GreenMate AI", "status": "online", "message": "Backend API Ready"})

# Global 404 Exception Handler for FastAPI / Starlette
@app.exception_handler(StarletteHTTPException)
async def custom_404_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        if request.url.path.startswith("/api"):
            return JSONResponse(status_code=404, content={"detail": exc.detail or "Not Found"})
        
        req_path = request.url.path.strip("/").split("?")[0]
        if req_path and frontend_dir.exists():
            html_candidate = frontend_dir / f"{req_path}.html"
            if html_candidate.exists():
                return FileResponse(html_candidate)
            file_candidate = frontend_dir / req_path
            if file_candidate.is_file() and file_candidate.exists():
                return FileResponse(file_candidate)
        
        if (frontend_dir / "index.html").exists():
            return FileResponse(frontend_dir / "index.html")

    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
