from functools import wraps
from db.redis_client import get_key
from .tokens import verify_token
from flask import request, jsonify
from db.users import userIsAdmin
from .responses import token_missing

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token_header = request.headers.get("Authorization")
        if not token_header:
            return token_missing(logged_out=True)
        raw_token = token_header.split(' ')[1]
        token_payload = verify_token(raw_token)
        print(f"{token_payload = }")
        if (not token_payload) or (get_key(raw_token) == "revoked"):
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs | {'isAdmin' : userIsAdmin(token_payload['user_id'])})
    return decorated
