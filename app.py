from flask import Flask, request, jsonify
from api import process_email
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route("/classify_email", methods=["POST"])
def classify_email():
    try:
        data = request.get_json()
        email_body = data.get("email_body")

        if not email_body:
            return jsonify({"error": "Missing email_body"}), 400

        result = process_email(email_body)
        return jsonify(result), 200

    except Exception as e:
        logging.exception("Error processing the email")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
