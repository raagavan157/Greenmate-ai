"""
GreenMate AI – Comprehensive Vercel & Production Deployment Verification Suite
Tests all 11 critical paths requested by the deployment specification.
"""
import os
import sys
import tempfile
import json
from pathlib import Path

# Ensure root & backend are in sys.path
ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"
for p in [str(BACKEND_DIR), str(ROOT_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

# Set test environment
os.environ["VERCEL"] = "1"
os.environ["ENVIRONMENT"] = "production"

def run_all_tests():
    print("=" * 60)
    print("GreenMate AI – Vercel Deployment Test Runner")
    print("=" * 60)
    
    passed_tests = 0
    total_tests = 11

    # -------------------------------------------------------------
    # Test 1: Python Imports & Read-Only Simulation
    # -------------------------------------------------------------
    print("\n[Test 1/11] Verifying Python imports & read-only safety...")
    try:
        from backend.config import settings
        from backend.database import db_manager, get_db
        from backend.main import app as backend_app
        import api.index as api_index
        import main as root_main
        assert backend_app is not None, "backend_app is None"
        assert api_index.app is not None, "api_index.app is None"
        assert root_main.app is not None, "root_main.app is None"
        assert not str(settings.UPLOAD_DIR).startswith("/var/task"), f"UPLOAD_DIR unsafe: {settings.UPLOAD_DIR}"
        print("  -> SUCCESS: All entry points and configs imported without filesystem crash.")
        passed_tests += 1
    except Exception as e:
        print(f"  -> FAILED: Import error: {e}")

    # -------------------------------------------------------------
    # Test 2: FastAPI Application Initialization
    # -------------------------------------------------------------
    print("\n[Test 2/11] Verifying FastAPI Application Initialization...")
    try:
        from fastapi.testclient import TestClient
        client = TestClient(backend_app, raise_server_exceptions=False)
        assert client is not None
        routes = list(backend_app.openapi().get("paths", {}).keys())
        assert "/api/health" in routes, "Missing /api/health"
        assert "/api/plants" in routes, "Missing /api/plants"
        assert "/api/auth/register" in routes, "Missing /api/auth/register"
        print(f"  -> SUCCESS: FastAPI initialized with {len(routes)} active API routes.")
        passed_tests += 1
    except Exception as e:
        print(f"  -> FAILED: App init error: {e}")

    # -------------------------------------------------------------
    # Test 3: Root & HTML Frontend Routes
    # -------------------------------------------------------------
    print("\n[Test 3/11] Verifying Root and Static Frontend routing...")
    try:
        res_root = client.get("/")
        assert res_root.status_code == 200, f"Root returned {res_root.status_code}"
        assert "GreenMate" in res_root.text or "<!DOCTYPE" in res_root.text

        res_explore = client.get("/explore")
        assert res_explore.status_code == 200, f"/explore returned {res_explore.status_code}"

        res_admin = client.get("/admin")
        assert res_admin.status_code == 200, f"/admin returned {res_admin.status_code}"

        print("  -> SUCCESS: Frontend HTML pages served with 200 OK.")
        passed_tests += 1
    except Exception as e:
        print(f"  -> FAILED: Root route error: {e}")

    # -------------------------------------------------------------
    # Test 4: Health Check Endpoint
    # -------------------------------------------------------------
    print("\n[Test 4/11] Verifying Health Check Endpoint (/api/health)...")
    try:
        res = client.get("/api/health")
        assert res.status_code == 200, f"Status: {res.status_code}"
        data = res.json()
        assert data.get("status") == "healthy", f"Unexpected status: {data}"
        assert "database" in data, "Missing database key in health check"
        print(f"  -> SUCCESS: Health endpoint healthy. Database mode: {data['database']['mode']}")
        passed_tests += 1
    except Exception as e:
        print(f"  -> FAILED: Health check failed: {e}")

    # -------------------------------------------------------------
    # Test 5: MongoDB Connection & Fallback Engine
    # -------------------------------------------------------------
    print("\n[Test 5/11] Verifying Database Engine Initialization...")
    try:
        db = get_db()
        assert db is not None
        plants_col = db.get_collection("plants")
        count = plants_col.count_documents({})
        assert count > 0, "No plants found in database"
        print(f"  -> SUCCESS: Database active ({'Atlas' if db.is_atlas else 'Resilient Document Store'}), {count} plants found.")
        passed_tests += 1
    except Exception as e:
        print(f"  -> FAILED: Database engine error: {e}")

    # -------------------------------------------------------------
    # Test 6: Authentication Endpoints (Register & Login)
    # -------------------------------------------------------------
    print("\n[Test 6/11] Verifying Authentication API (/api/auth)...")
    try:
        import uuid
        test_email = f"test_{uuid.uuid4().hex[:6]}@greenmate.ai"
        reg_payload = {
            "name": "Vercel Tester",
            "email": test_email,
            "password": "Password@123"
        }
        res_reg = client.post("/api/auth/register", json=reg_payload)
        assert res_reg.status_code in [200, 201], f"Register failed: {res_reg.text}"
        token_data = res_reg.json()
        assert "access_token" in token_data, "No access_token returned"

        # Login test
        login_payload = {
            "email": test_email,
            "password": "Password@123"
        }
        res_login = client.post("/api/auth/login", json=login_payload)
        assert res_login.status_code == 200, f"Login failed: {res_login.text}"
        assert "access_token" in res_login.json(), "No access_token on login"
        print("  -> SUCCESS: Registration and Login successful, JWT token issued.")
        passed_tests += 1
    except Exception as e:
        print(f"  -> FAILED: Auth error: {e}")

    # -------------------------------------------------------------
    # Test 7: Plant Catalog API
    # -------------------------------------------------------------
    print("\n[Test 7/11] Verifying Plant Catalog API (/api/plants)...")
    try:
        res = client.get("/api/plants?limit=5")
        assert res.status_code == 200, f"Plants API failed: {res.status_code}"
        data = res.json()
        assert isinstance(data, list) and len(data) > 0, "Catalog returned empty"
        assert "name" in data[0] and "price" in data[0]
        print(f"  -> SUCCESS: Plant catalog returned {len(data)} plants.")
        passed_tests += 1
    except Exception as e:
        print(f"  -> FAILED: Plant catalog error: {e}")

    # -------------------------------------------------------------
    # Test 8: Image Upload & AI Identification Endpoint
    # -------------------------------------------------------------
    print("\n[Test 8/11] Verifying Image Upload & Identification (/api/ai/identify)...")
    try:
        from io import BytesIO
        from PIL import Image

        # Create a tiny 10x10 green image in memory
        img = Image.new("RGB", (10, 10), color="green")
        buf = BytesIO()
        img.save(buf, format="JPEG")
        buf.seek(0)

        files = {"file": ("test_leaf.jpg", buf, "image/jpeg")}
        res_ident = client.post("/api/ai/identify", files=files)
        assert res_ident.status_code == 200, f"Identify failed: {res_ident.text}"
        ident_data = res_ident.json()
        assert "common_name" in ident_data, "Missing common_name in response"
        assert "image_url" in ident_data, "Missing image_url in response"
        print(f"  -> SUCCESS: Image upload handled safely. Identified: {ident_data['common_name']}")
        passed_tests += 1
    except Exception as e:
        print(f"  -> FAILED: Upload & identify error: {e}")

    # -------------------------------------------------------------
    # Test 9: CORS Headers Verification
    # -------------------------------------------------------------
    print("\n[Test 9/11] Verifying CORS headers for deployed domains...")
    try:
        res_cors = client.options(
            "/api/plants",
            headers={
                "Origin": "https://greenmate-ai.vercel.app",
                "Access-Control-Request-Method": "GET"
            }
        )
        # Check either options or standard get with origin header
        res_get = client.get("/api/plants", headers={"Origin": "https://greenmate-ai.vercel.app"})
        allow_origin = res_get.headers.get("access-control-allow-origin")
        assert allow_origin in ["*", "https://greenmate-ai.vercel.app"], f"CORS header missing: {allow_origin}"
        print(f"  -> SUCCESS: CORS header present: access-control-allow-origin: {allow_origin}")
        passed_tests += 1
    except Exception as e:
        print(f"  -> FAILED: CORS check failed: {e}")

    # -------------------------------------------------------------
    # Test 10: Frontend API Configuration Check
    # -------------------------------------------------------------
    print("\n[Test 10/11] Verifying Frontend API Client configuration...")
    try:
        api_js_path = ROOT_DIR / "frontend" / "js" / "api.js"
        assert api_js_path.exists(), "frontend/js/api.js does not exist"
        with open(api_js_path, "r", encoding="utf-8") as f:
            code = f.read()
        assert "GREENMATE_API_URL" in code, "Missing GREENMATE_API_URL override support"
        print("  -> SUCCESS: Frontend API client supports dynamic and configurable backend URLs.")
        passed_tests += 1
    except Exception as e:
        print(f"  -> FAILED: Frontend API config error: {e}")

    # -------------------------------------------------------------
    # Test 11: Vercel Configuration & Dependencies Verification
    # -------------------------------------------------------------
    print("\n[Test 11/11] Verifying vercel.json & requirements.txt...")
    try:
        vercel_json_path = ROOT_DIR / "vercel.json"
        assert vercel_json_path.exists(), "vercel.json missing"
        with open(vercel_json_path, "r", encoding="utf-8") as f:
            v_data = json.load(f)
        assert "rewrites" in v_data, "vercel.json missing rewrites"

        req_path = ROOT_DIR / "requirements.txt"
        assert req_path.exists(), "requirements.txt missing"
        with open(req_path, "r", encoding="utf-8") as f:
            reqs = f.read()
        for dep in ["fastapi", "uvicorn", "pymongo", "certifi", "cloudinary"]:
            assert dep in reqs, f"Missing {dep} in requirements.txt"

        print("  -> SUCCESS: vercel.json and requirements.txt are complete and valid.")
        passed_tests += 1
    except Exception as e:
        print(f"  -> FAILED: Configuration error: {e}")

    print("\n" + "=" * 60)
    print(f"TEST RESULTS: {passed_tests}/{total_tests} PASSED")
    print("=" * 60)
    
    if passed_tests == total_tests:
        print("ALL TESTS PASSED SUCCESSFULLY! Ready for Vercel deployment.")
        return 0
    else:
        print("SOME TESTS FAILED! Please inspect errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())
