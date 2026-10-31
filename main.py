import os
import sys
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

# Explicit top-level declarations satisfying Vercel AST entrypoint scanner
app = None
handler = None
application = None

try:
    from backend.main import app as _fastapi_app
    app = _fastapi_app
    handler = _fastapi_app
    application = _fastapi_app
except Exception as _exc:
    import traceback
    _err_msg = (
        f"GreenMate AI Serverless Startup Error:\n\n{traceback.format_exc()}\n\n"
        f"sys.path:\n" + "\n".join(sys.path)
    )
    print(_err_msg, file=sys.stderr)

    async def _fallback_app(scope, receive, send):
        if scope.get("type") == "http":
            await send({
                "type": "http.response.start",
                "status": 500,
                "headers": [[b"content-type", b"text/plain; charset=utf-8"]],
            })
            await send({
                "type": "http.response.body",
                "body": _err_msg.encode("utf-8"),
            })

    app = _fallback_app
    handler = _fallback_app
    application = _fallback_app

if __name__ == "__main__":
    import uvicorn
    from backend.config import settings
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
