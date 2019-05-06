from flask import Flask, send_from_directory, request
import json
import datetime

app = Flask(__name__)

@app.route("/")
def hello():
    return send_from_directory(directory="", filename="index.html")

@app.route("/upload", methods=['POST'])
def upload():
    image_file = request.files["file"]
    path = "images/" + image_file.filename
    image_file.save(path)
    return json.dumps({"path":path})




