from flask import Flask

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def login():
    return "Welcome to Fashion Paradise."
