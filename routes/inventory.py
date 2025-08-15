from flask import Blueprint, jsonify, request
from db.inventory import get_items

inventory_bp = Blueprint("inventory", __name__, url_prefix='/inventory')


@inventory_bp.route('/getItems')
def getItems():
    #add token verification
    # user = verify(token = ..., refresh = bool) -> User
    # return getItems(User.isAdmin())
    return jsonify(get_items(request.args.get('admin'))), 200

