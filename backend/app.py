import os
import requests
import resend
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL") + "/rest/v1/"
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
RESEND_API_KEY = os.getenv("RESEND_API_KEY")

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# Initialize Resend API
resend.api_key = RESEND_API_KEY


def send_verification_email(email):
    verify_link = f"https://your-frontend-url/verify?email={email}"
    resend.Emails.send({
        "from": "ByteSize <noreply@bytesize.app>",
        "to": email,
        "subject": "Verify Your Email for ByteSize",
        "html": f"<p>Click <a href='{verify_link}'>here</a> to verify your email and start receiving newsletters.</p>"
    })


@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.json
    email, source = data['email'], data['source']

    # Check if email already exists
    response = requests.get(f"{SUPABASE_URL}users?email=eq.{email}", headers=HEADERS)
    if response.json():
        return jsonify({"message": "Email already registered!"}), 400

    # Store email in Supabase (unverified)
    payload = {"email": email, "source": source, "verified": False}
    response = requests.post(f"{SUPABASE_URL}users", json=payload, headers=HEADERS)

    if response.status_code == 201:
        send_verification_email(email)
        return jsonify({"message": "Check your email to verify!"})
    
    return jsonify({"error": "Failed to subscribe"}), 400


@app.route('/verify', methods=['GET'])
def verify_email():
    email = request.args.get("email")

    if not email:
        return jsonify({"error": "Invalid verification request"}), 400

    # Update user as verified in Supabase
    payload = {"verified": True}
    response = requests.patch(f"{SUPABASE_URL}users?email=eq.{email}", json=payload, headers=HEADERS)

    if response.status_code == 200:
        return jsonify({"message": "Email verified successfully! You will now receive newsletters."})
    return jsonify({"error": "Verification failed"}), 400


if __name__ == '__main__':
    app.run(debug=True)
