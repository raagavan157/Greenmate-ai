import os
import sys
import traceback
from pathlib import Path

# Add backend and root directories to sys.path
current_dir = Path(__file__).resolve().parent
root_dir = current_dir.parent if current_dir.name == "api" else current_dir
backend_dir = root_dir / "backend"

for d in [str(backend_dir), str(root_dir)]:
    if d not in sys.path:
        sys.path.insert(0, d)

# Mark serverless environment
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
