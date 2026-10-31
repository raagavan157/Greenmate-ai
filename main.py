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

# Import existing FastAPI application
from backend.main import app

if __name__ == "__main__":
    import uvicorn
    from backend.config import settings
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
