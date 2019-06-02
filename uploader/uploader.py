from flask import Flask, send_from_directory, request, send_file
import json, datetime, sqlite3, os

def create_app(image_dir):
    app = Flask(__name__)

    if image_dir != None:
         image_dir = "images"
    app.config["IMAGE_DIR"] = image_dir

    @app.route("/")
    def index():
        return send_from_directory(directory="", filename="index.html")

if __name__ == "__main__":
    app = create_app()