from flask import jsonify
from .tokens import getKey
from auth import auth_bp


@auth_bp.route("/tmpKey", methods=["GET"])
def get_temp_key():
    kid, public_key = getKey()
    return jsonify({"kid": kid, "public_key": public_key.decode()}), 200
