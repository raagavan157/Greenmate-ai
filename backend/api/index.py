import os
import sys
import traceback
from pathlib import Path

backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

os.environ["VERCEL"] = "1"

try:
    from main import app
except Exception as e:
    _err_text = (
        f"GreenMate AI Backend Serverless Startup Error:\n\n"
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
