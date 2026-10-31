import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load .env
load_dotenv(Path(__file__).resolve().parent / ".env")

mongo_uri = os.getenv("MONGO_URI", "")
db_name = os.getenv("DB_NAME", "greenmate_db")

print("==================================================")
print("GreenMate AI - MongoDB Connection Test")
print("==================================================")

if not mongo_uri or "<db_username>" in mongo_uri or "your_" in mongo_uri:
    print("\n[!] Setup Needed: MONGO_URI is not configured yet in .env")
    print(f"Current MONGO_URI: {mongo_uri}")
    print("\nPlease open the .env file in the project folder and replace:")
    print("  <db_username> with your MongoDB database username")
    print("  <password> with your MongoDB database user password")
    print("\nExample:")
    print("  MONGO_URI=mongodb+srv://admin:MySecretPass123@cluster0.abcde.mongodb.net/greenmate_db?retryWrites=true&w=majority")
    sys.exit(1)

try:
    from pymongo import MongoClient
    print(f"\nConnecting to MongoDB database '{db_name}'...")
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000, connectTimeoutMS=5000)
    
    # Test ping
    client.admin.command('ping')
    print("[SUCCESS] Successfully connected to MongoDB Atlas!")
    
    db = client[db_name]
    collections = db.list_collection_names()
    print(f"[OK] Database '{db_name}' reachable. Collections found: {len(collections)}")
    if collections:
        print("     " + ", ".join(collections))
    else:
        print("     (Database is new and will be automatically seeded on server startup)")
    print("==================================================")

except Exception as e:
    err_str = str(e)
    print(f"\n[ERROR] Connection failed: {err_str}\n")
    if "bad auth" in err_str.lower() or "authentication failed" in err_str.lower():
        print("-> Cause: Invalid MongoDB Username or Password.")
        print("-> Fix: Check Database Access in MongoDB Atlas and verify your user credentials.")
    elif "serverselectiontimeouterror" in err_str.lower() or "timed out" in err_str.lower():
        print("-> Cause: IP Address not whitelisted on MongoDB Atlas.")
        print("-> Fix: In MongoDB Atlas, go to Network Access -> Add IP Address -> Select 'Allow Access From Anywhere' (0.0.0.0/0).")
    elif "dns" in err_str.lower():
        print("-> Cause: DNS resolution issue.")
        print("-> Fix: Check your internet connection or use a standard mongodb:// connection string.")
    print("==================================================")
    sys.exit(1)
