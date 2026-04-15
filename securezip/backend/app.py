from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import time
from werkzeug.utils import secure_filename
from utils.image_compress import compress_image
from utils.pdf_compress import compress_pdf

app = Flask(__name__)
CORS(app)

# --- CONFIGURATION ---
# Using abspath ensures Ghostscript gets the full system path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "output")

# Ensure directories exist on startup
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def get_extension(filename):
    """Extracts the file extension in lowercase."""
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

@app.route("/upload", methods=["POST"])
def upload_file():
    # 1. Validation
    file = request.files.get("file")
    compression = request.form.get("compression", "Recommended Compression")

    if not file or file.filename == '':
        return jsonify({"error": "No file uploaded"}), 400

    # 2. Secure Filename & Unique Timestamp
    # This prevents directory traversal attacks and filename collisions
    original_name = secure_filename(file.filename)
    timestamp = int(time.time())
    unique_name = f"{timestamp}_{original_name}"
    
    # 3. Define Absolute Paths
    input_path = os.path.abspath(os.path.join(UPLOAD_FOLDER, unique_name))
    
    ext = get_extension(original_name)
    output_filename = f"compressed_{unique_name}"
    output_path = os.path.abspath(os.path.join(OUTPUT_FOLDER, output_filename))

    try:
        # Save the uploaded file
        file.save(input_path)

        # 4. Process based on extension
        if ext in ["jpg", "jpeg", "png"]:
            compress_image(input_path, output_path, compression)
        elif ext == "pdf":
            # Passing absolute paths is critical for Ghostscript (gs)
            compress_pdf(input_path, output_path, compression)
        else:
            # Clean up uploaded file if not supported
            if os.path.exists(input_path):
                os.remove(input_path)
            return jsonify({"error": f"Unsupported file type: {ext}"}), 400
            
    except Exception as e:
        # Log the error for debugging
        print(f"Error processing file: {str(e)}")
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

    # 5. Success Response
    return jsonify({
        "message": f"{ext.upper()} processed successfully",
        "downloadUrl": f"http://127.0.0.1:5000/download/{output_filename}"
    })

@app.route("/download/<filename>")
def download_file(filename):
    # Security: prevent users from accessing files outside the output folder
    safe_name = secure_filename(filename)
    path = os.path.abspath(os.path.join(OUTPUT_FOLDER, safe_name))
    
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    
    return jsonify({"error": "File not found"}), 404

if __name__ == "__main__":
    # Running on 0.0.0.0 allows access from other devices on the same network
    app.run(debug=True, host="127.0.0.1", port=5000)