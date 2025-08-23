from functools import wraps
from db.redis_client import get_key
from .tokens import verify_token
from flask import request, jsonify
from db.users import userIsAdmin
from .responses import token_missing

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return token_missing(logged_out=True)
        data = verify_token(token.split(' ')[1])
        if not token or not data or get_key(token) == "revoked":
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs | {'isAdmin' : userIsAdmin(data['user_id'])})
    return decorated
