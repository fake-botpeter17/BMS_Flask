from flask import jsonify
from .tokens import generate_token
from utils.types import User
from db.redis_client import set_key
import datetime

def key_error():
    return jsonify({
            "error" : "expired_key",
            "expired": True,
            "status": "failure",
            "message" : "The key you used has expired. Please request for a new one."
        }), 401

def token_error():
    return jsonify({
            "error" : "expired_token",
            "expired": True,
            "status": "failure",
            "message" : "The token you used has expired. Please request for a new one."
        }), 401

def token_missing():
    return jsonify({
        "error": "unauthorized",
        "status": "failure",
        "message": "Missing Authorization header"
    }), 401

def auth_failed():
    return jsonify({
        "error": "failed_auth",
        "status": "failure",
        "message": "User Credentials are invalid."
    }), 401

def user_authenticated(user: User):
    res = {
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
    set_key(res["refresh_token"], user.uid, expire=res["refresh_expires_in"])
    return jsonify(res), 200

def token_refreshed(user: User):
    res = {
        "success": True,
        "access_token": generate_token(user.uid),
        "refresh_token": generate_token(user.uid, refresh=True),
        "token_type": 'Bearer',
        "iat": datetime.datetime.now(datetime.timezone.utc),
        "expires_in": 30*60,
        "refresh_expires_in": 7*24*60*60,
        "message": "Refresh Successful"
    }
    set_key(res["refresh_token"], user.uid, expire=res["refresh_expires_in"])
    return jsonify(res), 200

