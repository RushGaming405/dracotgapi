from flask import Flask, jsonify
import re
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE = os.path.join(BASE_DIR, "INDIAN_TG_NUMBERS.txt")

OWNER = "t.me/optimusprine50"
CHANNEL = "t.me/primedraco12"


def load_users():
    users = []

    if not os.path.exists(FILE):
        return users

    with open(FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            user_id = re.search(r"User ID:\s*(\d+)", line)
            phone = re.search(r"Phone:\s*(\d+)", line)
            username = re.search(r"Username:\s*(.*)$", line)

            if user_id:
                users.append({
                    "user_id": user_id.group(1),
                    "phone": phone.group(1) if phone else None,
                    "username": (
                        username.group(1).strip()
                        if username else None
                    )
                })

    return users


@app.route("/")
def home():
    return jsonify({
        "success": True,
        "message": "Dummy Test API is running",
        "owner": OWNER,
        "channel": CHANNEL,
        "endpoint": "/api/user/<user_id>"
    })


@app.route("/api/user/<user_id>")
def get_user(user_id):
    if not user_id.isdigit():
        return jsonify({
            "success": False,
            "message": "Invalid user ID"
        }), 400

    for user in load_users():
        if user["user_id"] == user_id:
            return jsonify({
                "success": True,
                "data": user,
                "owner": OWNER,
                "channel": CHANNEL
            })

    return jsonify({
        "success": False,
        "message": "User ID not found",
        "owner": OWNER,
        "channel": CHANNEL
    }), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
