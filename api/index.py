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
