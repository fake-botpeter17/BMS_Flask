from flask import jsonify, request
from db.users import getUser
from .tokens import getKey, verify_token
from .responses import token_error, token_refreshed, token_missing
from db.redis_client import delete_key, get_key
from auth import auth_bp


@auth_bp.route("/tmpKey", methods=["GET"])
def get_temp_key():
    kid, public_key = getKey()
    return jsonify({"kid": kid, "public_key": public_key.decode()}), 200


@auth_bp.route("/refresh", methods=["POST"])
def refresh_token():
    refresh_token = request.cookies.get('refresh_token')

    if not refresh_token:
        return token_missing()

    data = verify_token(refresh_token)

    if data is None:
        return token_error()

    if get_key(refresh_token) != data["user_id"]:
        return token_error()

    user = getUser(data["user_id"],obj=True)
    delete_key(refresh_token)
    return token_refreshed(user)
