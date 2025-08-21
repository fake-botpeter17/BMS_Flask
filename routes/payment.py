from os import getenv
from app import socket
from flask import jsonify, Blueprint, render_template, request
from auth.decorators import require_auth
from utils.misc import generate_qr_base64

payment_bp = Blueprint("payment", __name__, url_prefix="/payment")

@payment_bp.route("/show_qr")
def qr_pay():
    return render_template('qr.html')

@payment_bp.route('/testQR')
@require_auth
def send_qr_details():
    amount = request.args.get('amount')
    URI = (f"upi://pay?pa={getenv("PA")}&pn={getenv("PN")}&am={float(amount)}&cu={getenv("CU")}&tn={""}&mc={getenv("MC")}&mode=04")
    socket.emit('set_qr',{"qrData": generate_qr_base64(URI), "duration":300, "amount":amount})
    return jsonify(None)


@payment_bp.route('/success')
@require_auth
def success():
    socket.emit('payment_success')
    return {"Success": True}