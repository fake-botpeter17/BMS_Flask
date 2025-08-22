from flask import Flask, render_template
from flask_socketio import SocketIO
from routes.inventory import inventory_bp
from auth.routes import auth_bp

app = Flask(__name__)
socket = SocketIO(app)
from routes.payment import payment_bp
app.register_blueprint(inventory_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(payment_bp)


@app.route("/", methods=["GET"])
def login():
    return render_template("login.html")
