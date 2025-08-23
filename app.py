from flask import Flask, render_template, request
from flask_socketio import SocketIO
from auth.decorators import require_auth
from auth.responses import token_error
from auth.tokens import verify_token
from db.users import getUser
from routes.inventory import inventory_bp
from auth.routes import auth_bp
from routes.billing import billing_bp
from utils.types import User

app = Flask(__name__)
socket = SocketIO(app)
from routes.payment import payment_bp
app.register_blueprint(inventory_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(payment_bp)
app.register_blueprint(billing_bp)


@app.route("/", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/me")
@require_auth
def user_info(**kwargs):
    token = request.headers.get("Authorization").split(" ")[1]
    token_payload = verify_token(token)
    if not token_payload: 
        return token_error()
    uid = token_payload["user_id"]
    return User(**getUser(uid)).model_dump()