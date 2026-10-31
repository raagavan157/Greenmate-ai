import os
import sys
from pathlib import Path

backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

os.environ["VERCEL"] = "1"

# Explicit top-level declarations satisfying Vercel AST entrypoint scanner
app = None
handler = None
application = None

try:
    from main import app as _fastapi_app
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
