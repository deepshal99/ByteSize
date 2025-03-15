import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable frontend-backend communication

# Load Supabase API Credentials
SUPABASE_URL = os.getenv("SUPABASE_URL") + "/rest/v1/"
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# Route to handle user subscriptions
@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.json
    email, source = data['email'], data['source']

    # Check if email already exists
    response = requests.get(
        f"{SUPABASE_URL}users?email=eq.{email}",
        headers=HEADERS
    )

    if response.json():  # If email exists, return message
        return jsonify({"message": "Email already registered!"}), 400

    # Insert new user data into Supabase
    payload = {"email": email, "source": source, "verified": False}
    response = requests.post(f"{SUPABASE_URL}users", json=payload, headers=HEADERS)

    if response.status_code == 201:
        return jsonify({"message": "Check your email to verify!"})
    return jsonify({"error": "Failed to subscribe"}), 400


# Route to fetch all users (for debugging)
@app.route('/users', methods=['GET'])
def get_users():
    response = requests.get(f"{SUPABASE_URL}users", headers=HEADERS)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
