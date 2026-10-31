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
    _err_text = (
        f"GreenMate AI Serverless Startup Error:\n\n"
        f"{traceback.format_exc()}\n\n"
        f"Python Version: {sys.version}\n"
        f"sys.path:\n" + "\n".join(sys.path)
    )

    class ErrorApp:
        async def __call__(self, scope, receive, send):
            await send({
                "type": "http.response.start",
                "status": 500,
                "headers": [[b"content-type", b"text/plain; charset=utf-8"]],
            })
            await send({
                "type": "http.response.body",
                "body": _err_text.encode("utf-8"),
            })

    app = ErrorApp()

if __name__ == "__main__":
    import uvicorn
    from backend.config import settings
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
