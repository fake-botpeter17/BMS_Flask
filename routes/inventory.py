from flask import Blueprint, jsonify
from db.inventory import get_items
from auth.decorators import require_auth

inventory_bp = Blueprint("inventory", __name__, url_prefix='/inventory')


@inventory_bp.route('/getItems')
@require_auth
def getItems(**kwargs):
    return jsonify(get_items(**kwargs)), 200

