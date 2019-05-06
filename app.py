from flask import Flask, send_from_directory, request, jsonify
import datetime

app = Flask(__name__)

@app.route("/")
def hello():
    return send_from_directory(directory="", filename="index.html")