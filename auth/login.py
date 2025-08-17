from flask import request
from auth import auth_bp
from json import loads
from auth.decorators import require_auth
from db.users import getUser, authenticated
from .tokens import (
    getPrivateKey,
    decrypt_with_private_key,
    revokeKey
)
from utils.types import User
from .responses import auth_failed, key_error, user_authenticated, token_missing, user_logged_out


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
        return auth_failed()
    if authenticated(user, password):
        revokeKey(kid)
        return user_authenticated(User(**user))
    return auth_failed()


@auth_bp.route('/logout')
@require_auth
def logout():
    refresh = request.cookies.get('refresh_token')
    if not refresh:
        return token_missing()
    revokeKey(refresh)
    return user_logged_out()
