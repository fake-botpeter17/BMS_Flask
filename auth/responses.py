from flask import jsonify
from .tokens import generate_token
from utils.types import User
import datetime

def key_error():
    return jsonify({
            "error" : "expired_key",
            "expired": True,
            "status": "failure",
            "message" : "The key you used has expired. Please request for a new one."
        }), 401

def auth_failed():
    return jsonify({
        "error": "failed_auth",
        "status": "failure",
        "message": "User Credentials are invalid."
    }), 401

def user_authenticated(user: User):
    return jsonify(
            {
                "success": True, 
                "access_token": generate_token(user.uid),
                "refresh_token": generate_token(user.uid, refresh=True),
                "token_type": 'Bearer',
                "iat": datetime.datetime.now(datetime.timezone.utc),
                "expires_in": 30*60,
                "refresh_expires_in": 7*24*60*60,
                "user": user.model_dump(),
                "message": "Authentication Successful"
            }
        ), 200