from flask import Flask, request, jsonify
import json, os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATA_DIR = "data"
ACCOUNTS_FILE = os.path.join(DATA_DIR, "accounts.json")
LOG_FILE = os.path.join(DATA_DIR, "logs.json")
API_KEY = "admin-secret-key"

os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(ACCOUNTS_FILE):
    with open(ACCOUNTS_FILE, "w", encoding="utf-8") as f:
        json.dump({"admin": {"pwd": "123", "role": "admin", "disabled": False}}, f, indent=2)
@app.route("/ping", methods=["GET"])
def ping():
    return "pong", 200

@app.before_request
def check_api_key():
    key = request.headers.get("Authorization")
    if key != "Bearer admin-secret-key":
        return jsonify({"error": "Unauthorized"}), 401

@app.route("/accounts", methods=["GET"])
def get_accounts():
    with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
        return jsonify(json.load(f))

@app.route("/accounts", methods=["POST"])
def add_account():
    data = request.json
    with open(ACCOUNTS_FILE, "r+", encoding="utf-8") as f:
        accounts = json.load(f)
        if data["username"] in accounts:
            return jsonify({"error": "User exists"}), 400
        accounts[data["username"]] = {
            "pwd": data["pwd"],
            "role": data.get("role", "user"),
            "disabled": False
        }
        f.seek(0)
        json.dump(accounts, f, indent=2)
        f.truncate()
    return jsonify({"message": "User added"})

@app.route("/accounts/<username>", methods=["PUT"])
def update_account(username):
    data = request.json
    with open(ACCOUNTS_FILE, "r+", encoding="utf-8") as f:
        accounts = json.load(f)
        if username not in accounts:
            return jsonify({"error": "User not found"}), 404
        accounts[username].update(data)
        f.seek(0)
        json.dump(accounts, f, indent=2)
        f.truncate()
    return jsonify({"message": "User updated"})

@app.route("/logs", methods=["GET"])
def get_logs():
    if not os.path.exists(LOG_FILE):
        return jsonify([])
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return jsonify(json.load(f))
if __name__ == "__main__":
    from keep_alive import keep_alive_loop
    import threading

    threading.Thread(target=keep_alive_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=3000)
