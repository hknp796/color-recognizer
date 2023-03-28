# save this as app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import imageRead

app = Flask(__name__)

CORS(app)


@app.route("/image", methods=["POST"])
def image_route():
    file = request.files["file"]
    file_path = "path/cut.png"  # replace with the path to save the uploaded image
    file.save(file_path)
    result = imageRead.image_read(file_path)
    return jsonify({"string": result})


if __name__ == "__main__":
    app.run(debug=True)
