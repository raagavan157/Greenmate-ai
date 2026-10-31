import os
import sys
import traceback
from pathlib import Path

# Add backend directory to sys.path
root_dir = Path(__file__).resolve().parent
backend_dir = root_dir / "backend"

for d in [str(backend_dir), str(root_dir)]:
    if d not in sys.path:
        sys.path.insert(0, d)

# Mark serverless environment if running under AWS Lambda/Vercel
if os.getenv("VERCEL") or "/var/task" in str(Path(__file__).resolve()):
    os.environ["VERCEL"] = "1"

try:
    from backend.main import app
except Exception as e:
    from fastapi import FastAPI
    from fastapi.responses import PlainTextResponse

    app = FastAPI(title="GreenMate AI - Diagnostic Fallback")
    _err_trace = traceback.format_exc()

    @app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"])
    def boot_error_handler(path: str = ""):
        return PlainTextResponse(
            f"GreenMate AI Serverless Startup Diagnostics:\n\n{_err_trace}\n\nSys.path:\n" + "\n".join(sys.path),
            status_code=500
        )

if __name__ == "__main__":
    import uvicorn
    from backend.config import settings
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
