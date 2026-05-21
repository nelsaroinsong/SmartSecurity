import os
from datetime import datetime, timezone
from collections import deque
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

MAX_EVENTS = 200
EVENTS = deque(maxlen=MAX_EVENTS)
LATEST_STATUS = {
    "device_id": "unknown",
    "motion": False,
    "updated_at": None,
    "total_events": 0,
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@app.route("/")
def dashboard():
    return render_template("index.html")


@app.route("/api/motion", methods=["POST"])
def receive_motion():
    data = request.get_json(silent=True) or {}
    device_id = str(data.get("device_id", "unknown"))
    motion = bool(data.get("motion", False))
    ts = now_iso()

    event = {
        "device_id": device_id,
        "motion": motion,
        "timestamp": ts,
    }
    EVENTS.appendleft(event)

    LATEST_STATUS["device_id"] = device_id
    LATEST_STATUS["motion"] = motion
    LATEST_STATUS["updated_at"] = ts
    LATEST_STATUS["total_events"] += 1

    return jsonify({"ok": True, "received": event}), 200


@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "status": LATEST_STATUS,
        "events": list(EVENTS)[:30],
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"ok": True})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
