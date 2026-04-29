from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import time
from werkzeug.utils import secure_filename
from utils.image_compress import compress_image
from utils.pdf_compress import compress_pdf

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "output")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def get_extension(filename):
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    compression = request.form.get("compression", "Recommended Compression")
    if not file or file.filename == '':
        return jsonify({"error": "No file uploaded"}), 400
    original_name = secure_filename(file.filename)
    timestamp = int(time.time())
    unique_name = f"{timestamp}_{original_name}"
    input_path = os.path.abspath(os.path.join(UPLOAD_FOLDER, unique_name))
    ext = get_extension(original_name)
    output_filename = f"compressed_{unique_name}"
    output_path = os.path.abspath(os.path.join(OUTPUT_FOLDER, output_filename))

    try:
        file.save(input_path)

        if ext in ["jpg", "jpeg", "png"]:
            compress_image(input_path, output_path, compression)
        elif ext == "pdf":
            compress_pdf(input_path, output_path, compression)
        else:
            if os.path.exists(input_path):
                os.remove(input_path)
            return jsonify({"error": f"Unsupported file type: {ext}"}), 400
            
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

    return jsonify({
        "message": f"{ext.upper()} processed successfully",
        "downloadUrl": f"http://127.0.0.1:5000/download/{output_filename}"
    })
@app.route("/download/<filename>")
def download_file(filename):
    safe_name = secure_filename(filename)
    path = os.path.abspath(os.path.join(OUTPUT_FOLDER, safe_name))    
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    
    return jsonify({"error": "File not found"}), 404

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)