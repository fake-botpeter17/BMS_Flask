from flask import jsonify
from .tokens import generate_token
from utils.types import User
from db.redis_client import set_key
import datetime


def key_error():
    return jsonify(
        {
            "error": "expired_key",
            "expired": True,
            "status": "failure",
            "message": "The key you used has expired. Please request for a new one.",
        }
    ), 401


def token_error():
    return jsonify(
        {
            "error": "expired_token",
            "expired": True,
            "status": "failure",
            "message": "The token you used has expired. Please request for a new one.",
        }
    ), 401


def token_missing(logged_out = False):
    return jsonify(
        {
            "error": "unauthorized",
            "status": "failure",
            "message": "Missing Refresh Token",
            "logged_out": logged_out
        }
    ), 401


def auth_failed():
    return jsonify(
        {
            "error": "failed_auth",
            "status": "failure",
            "message": "User Credentials are invalid.",
        }
    ), 401


def user_authenticated(user: User):
    data = {
        "success": True,
        "access_token": generate_token(user.uid),
        "token_type": "Bearer",
        "iat": datetime.datetime.now(datetime.timezone.utc),
        "expires_in": 30 * 60,
        "user": user.model_dump(),
        "message": "Authentication Successful",
    }
    refresh_token = generate_token(user.uid, refresh=True)
    res = jsonify(data)
    print(f"User authenticated: {data}")
    res.set_cookie(
        "refresh_token",
        refresh_token,
        max_age=7 * 24 * 60 * 60,
        httponly=True,
        secure=True,
        samesite="strict",
    )
    set_key(refresh_token, user.uid, expire=7 * 24 * 60 * 60)
    return res, 200


def token_refreshed(user: User):
    res = jsonify(
        {
            "success": True,
            "access_token": generate_token(user.uid),
            "token_type": "Bearer",
            "iat": datetime.datetime.now(datetime.timezone.utc),
            "expires_in": 30 * 60,
            "message": "Refresh Successful",
        }
    )
    refresh_token = generate_token(user.uid, refresh=True)
    res.set_cookie(
        "refresh_token",
        refresh_token,
        max_age=7 * 24 * 60 * 60,
        httponly=True,
        secure=True,
        samesite="strict",
    )
    set_key(refresh_token, user.uid, expire=7 * 24 * 60 * 60)
    return res, 200

def user_logged_out():
    return jsonify({
        "success": True,
        "message": "Logout successful",
        "logged_out" : True
    }), 200