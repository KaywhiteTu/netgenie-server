import requests
import time

SERVER_URL = "https://netgenie-server.onrender.com/ping"

def keep_alive_loop():
    while True:
        try:
            print("🟢 Pinging server...")
            res = requests.get(SERVER_URL, timeout=3)
            print(f"✅ Response: {res.status_code}")
        except Exception as e:
            print(f"❌ Ping failed: {e}")
        time.sleep(600)  # ping mỗi 10 phút