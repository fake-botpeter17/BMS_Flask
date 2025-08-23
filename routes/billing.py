from flask import Blueprint, jsonify, render_template
from auth.decorators import require_auth
from db.billing import get_latest_bill_no

billing_bp = Blueprint("billing", __name__, url_prefix="/billing")


@billing_bp.route("/getLastBillNo")
@require_auth
def last_bill_no(**kwargs):
    return jsonify(get_latest_bill_no())


@billing_bp.route('/')
def billing_page():
    return render_template("billing.html")