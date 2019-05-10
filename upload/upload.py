from flask import Flask, send_from_directory, request, send_file
import json, datetime, sqlite3, os

def write_log(database_file, result, path):
    try:     
        con = sqlite3.connect(database_file)
        cur = con.cursor()
        cur.execute("INSERT INTO upload_result(date, result, path) VALUES (?,?,?)", \
            (datetime.datetime.now(), result, path))
        con.commit()
    except:
        con.rollback()
    finally:
        con.close()

def init_db(database_file):
    create_query = "CREATE TABLE IF NOT EXISTS upload_result(date TEXT, result TEXT, path TEXT)"
    with sqlite3.connect(database_file) as conn:
        c = conn.cursor()
        c.execute(create_query)

def create_app():
    image_dir = "images"
    database_file = 'upload_result.db'

    app = Flask(__name__)
    app.config["DATABASE"] = database_file
    app.config["IMAGE_DIR"] = image_dir

    @app.route("/")
    def index():
        return send_from_directory(directory="", filename="index.html")

    @app.route("/upload", methods=['POST'])
    def upload():
        if "file" not in request.files:
            result = "Cannot find file"
            write_log(result, None, app.config["DATABASE"])
            return "", 400

        image_file = request.files["file"]

        if image_file.filename == None:
            result = "File name is empty"
            write_log(result, None, app.config["DATABASE"])
            return "", 400

        path = "{0}/{1}".format(app.config["IMAGE_DIR"], image_file.filename)
        image_file.save(path)
        write_log(app.config["DATABASE"], "Success", path)
        return json.dumps({"path":path}), 200

    @app.route("/images/<name>")
    def image(name):
        return send_from_directory(directory="../" + app.config["IMAGE_DIR"], filename=name)

    return app


if __name__ == "__main__":
    app = create_app()