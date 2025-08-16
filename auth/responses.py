from flask import jsonify


def key_error():
    return jsonify({
            "error" : "expired_key",
            "expired": True,
            "message" : "The key you used has expired. Please request for a new one."
        }), 401