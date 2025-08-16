from flask import Blueprint, jsonify, request
from db.inventory import get_items
from auth.decorators import require_auth

inventory_bp = Blueprint("inventory", __name__, url_prefix='/inventory')


@inventory_bp.route('/getItems')
@require_auth
def getItems():
    return jsonify(get_items(request.args.get('admin'))), 200

