import os
import sys
from pathlib import Path

# Add backend and root directories to sys.path
current_dir = Path(__file__).resolve().parent
root_dir = current_dir.parent
backend_dir = root_dir / "backend"

for d in [str(backend_dir), str(root_dir)]:
    if d not in sys.path:
        sys.path.insert(0, d)

# Mark serverless environment
os.environ["VERCEL"] = "1"

# Import existing FastAPI application
from backend.main import app
