from flask import Flask, jsonify
from flask_cors import CORS
import json
import logging

# Silence the standard Flask startup text for a cleaner terminal
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
# [CORS] The Shield of Ogún: Allows your React frontend to connect securely
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        # Read the latest pulse written by Sentinel Apex Core
        with open('sentinel_state.json', 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": True, "message": str(e)}), 500

if __name__ == '__main__':
    print("--------------------------------------------------")
    print("[ÈṢÙ] API Bridge Online. Listening on Port 5000...")
    print("--------------------------------------------------")
    # Host 0.0.0.0 allows connections from your Cloudflare tunnel or localhost
    app.run(host='0.0.0.0', port=5000, debug=False)
