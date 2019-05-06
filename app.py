from flask import Flask, send_from_directory, request
import json
import datetime

image_dir = "images"
log_dir = "logs/upload-{0}.log".format(datetime.datetime.now())

app = Flask(__name__)

def write_log(result, path):
    with open(log_dir, 'a+') as log_file:
        log_content = "{0}|{1}|{2}\n".format(datetime.datetime.now(), result, path) 
        log_file.write(log_content)

@app.route("/")
def index():
    return send_from_directory(directory="", filename="index.html")

@app.route("/upload", methods=['POST'])
def upload():
    if "file" not in request.files:
        result = "Cannot find file"
        write_log(result, None)
        return "", 400

    image_file = request.files["file"]

    if image_file.filename == "":
        result = "File name is empty"
        write_log(result, None)
        return "", 400

    path = "{0}/{1}".format(image_dir, image_file.filename)
    image_file.save(path)
    write_log("Success", path)
    return json.dumps({"path":path}), 200

@app.route("/images/<name>")
def image(name):
    return send_from_directory(directory=image_dir, filename=name)


