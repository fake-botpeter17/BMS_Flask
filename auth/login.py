from flask import request, jsonify
from auth import auth_bp
from json import loads
from db.users import getUser, authenticated
from .tokens import (
    getPrivateKey,
    decrypt_with_private_key,
    revokeKey,
    generate_refresh_access_tokens,
)
from .responses import key_error
from utils.types import User


@auth_bp.route("/", methods=["POST"])
def authenticate_user():
    data = request.json
    kid = data.get("kid")
    private_key = getPrivateKey(kid)
    if private_key is None:
        return key_error()
    decrypted_data = loads(
        decrypt_with_private_key(private_key, data.get("encrypted_data"))
    )
    username = decrypted_data.get("username")
    password = decrypted_data.get("password")
    user = getUser(username)
    if user is None:
        return jsonify({"success": False})
    if authenticated(user, password):
        revokeKey(kid)
        return jsonify(
            User(**user).model_dump()
            | {"success": True}
            | generate_refresh_access_tokens(User(**user))
        ), 200
    return jsonify({"success": False})
