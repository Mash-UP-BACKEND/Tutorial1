from flask import Flask, send_from_directory, request
import json
import datetime

image_dir = "images"

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory(directory="", filename="index.html")

@app.route("/upload", methods=['POST'])
def upload():
    image_file = request.files["file"]
    path = "{0}/{1}".format(image_dir, image_file.filename)
    image_file.save(path)
    return json.dumps({"path":path})

@app.route("/images/<name>")
def image(name):
    return send_from_directory(directory=image_dir, filename=name)


