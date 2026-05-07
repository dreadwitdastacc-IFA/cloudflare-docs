import os
import json
import logging
from flask import Flask, jsonify
from flask_cors import CORS

try:
    from bitcoin_regtest_manager import BitcoinRegtestManager
except ImportError:
    BitcoinRegtestManager = None

STATE_FILE = os.path.join(os.path.dirname(__file__), 'sentinel_state.json')

# Silence the standard Flask startup text for a cleaner terminal
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
# [CORS] The Shield of Ogún: Allows your React frontend to connect securely
CORS(app, resources={r"/api/*": {"origins": "*"}})

COMPOSE_FILE = os.getenv('BITCOIN_REGTEST_COMPOSE', 'docker-compose.bitcoin-regtest.yml')


def get_bitcoin_manager():
    if BitcoinRegtestManager is None:
        return None
    return BitcoinRegtestManager(compose_file=os.path.abspath(COMPOSE_FILE))


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "service": "api_bridge", "bitcoin_regtest_compose": COMPOSE_FILE})


@app.route('/api/data', methods=['GET'])
def get_data():
    if not os.path.exists(STATE_FILE):
        return jsonify({"error": True, "message": f"State file not found: {STATE_FILE}"}), 404

    try:
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except json.JSONDecodeError as e:
        return jsonify({"error": True, "message": f"Failed to parse state file: {e}"}), 500
    except Exception as e:
        return jsonify({"error": True, "message": str(e)}), 500


@app.route('/api/state', methods=['GET'])
def get_state():
    return get_data()


@app.route('/api/bitcoin/regtest/status', methods=['GET'])
def bitcoin_regtest_status():
    manager = get_bitcoin_manager()
    if manager is None:
        return jsonify({"error": True, "message": "Bitcoin regtest manager not available"}), 501
    try:
        return jsonify({"status": manager.status_cluster()})
    except Exception as e:
        return jsonify({"error": True, "message": str(e)}), 500


@app.route('/api/bitcoin/regtest/start', methods=['POST'])
def bitcoin_regtest_start():
    manager = get_bitcoin_manager()
    if manager is None:
        return jsonify({"error": True, "message": "Bitcoin regtest manager not available"}), 501
    try:
        manager.start_cluster()
        return jsonify({"status": "started"})
    except Exception as e:
        return jsonify({"error": True, "message": str(e)}), 500


@app.route('/api/bitcoin/regtest/stop', methods=['POST'])
def bitcoin_regtest_stop():
    manager = get_bitcoin_manager()
    if manager is None:
        return jsonify({"error": True, "message": "Bitcoin regtest manager not available"}), 501
    try:
        manager.stop_cluster()
        return jsonify({"status": "stopped"})
    except Exception as e:
        return jsonify({"error": True, "message": str(e)}), 500


if __name__ == '__main__':
    print("--------------------------------------------------")
    print("[ÈṢÙ] API Bridge Online. Listening on Port 5000...")
    print("--------------------------------------------------")
    app.run(host='0.0.0.0', port=5000, debug=False)
