from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join("backend", "uploads")
OUTPUT_FOLDER = os.path.join("backend", "output")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    compression = request.form.get("compression", "Recommended Compression")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    return jsonify({
        "message": "File received",
        "compression": compression,
        "filename": file.filename
    })
if __name__ == "__main__":
    app.run(debug=True)