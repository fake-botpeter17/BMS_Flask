from functools import wraps
from .tokens import verify_token
from flask import request, jsonify
from db.users import userIsAdmin

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        data = verify_token(token)
        if not token or not data:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs | {'isAdmin' : userIsAdmin(data['user_id'])})
    return decorated
