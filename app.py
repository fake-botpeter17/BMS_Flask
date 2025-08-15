from flask import Flask, render_template
from routes.inventory import inventory_bp

app = Flask(__name__)
app.register_blueprint(inventory_bp)

@app.route('/', methods = ['GET'])
def login():
    return render_template('login.html')
