import subprocess
import os
import shutil
import tempfile

def compress_pdf(input_path, output_path, level):
    level = level.strip()
    gs_bin = shutil.which("gs")
    
    if not gs_bin:
        raise Exception("Ghostscript not found. Run: sudo apt install ghostscript")

    # 1. Map quality levels
    quality = "/screen" if level == "Extreme Compression" else "/ebook" if level == "Recommended Compression" else "/prepress"

    # 2. CREATE LOCAL TEMP PATHS (Inside native Linux storage)
    # We create a temp input AND a temp output to bypass /mnt/ issues entirely
    tmp_dir = tempfile.gettempdir()
    local_input = os.path.join(tmp_dir, f"in_{os.path.basename(input_path)}")
    local_output = os.path.join(tmp_dir, f"out_{os.path.basename(output_path)}")

    try:
        # 3. STAGE: Copy the file from /mnt/ to local /tmp/
        shutil.copy2(input_path, local_input)

        # 4. BUILD COMMAND (Using only local /tmp/ paths)
        command = [
            gs_bin,
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            f"-dPDFSETTINGS={quality}",
            "-dNOPAUSE",
            "-dBATCH",
            "-dQUIET",
            f"-sOutputFile={local_output}", 
            local_input
        ]

        # 5. EXECUTE
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        
        # 6. COMMIT: Move result from local /tmp/ back to your /mnt/ folder
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        shutil.move(local_output, output_path)
        
        return output_path

    except subprocess.CalledProcessError as e:
        print(f"--- GS DEBUG START ---\nSTDERR: {e.stderr}\nSTDOUT: {e.stdout}\n--- GS DEBUG END ---")
        raise Exception(f"Ghostscript Error: {e.stderr or 'Unrecoverable error'}")
        
    finally:
        # CLEANUP: Always remove the local temp files
        for f in [local_input, local_output]:
            if os.path.exists(f):
                os.remove(f)