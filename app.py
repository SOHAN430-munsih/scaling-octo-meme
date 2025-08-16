import os, random, time
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from flask_cors import CORS

from models.dummy_model import predict_from_bytes, predict_from_text

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)  # allow cross-origin requests (frontend on other domain)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50 MB

ALLOWED_EXT = {"png", "jpg", "jpeg", "webp", "txt", "csv"}

def allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT

@app.route("/", methods=["GET"])
def home():
    # Renders the upload + text form
    return render_template("index.html")

@app.route("/api/predict", methods=["POST"])
def api_predict():
    text = request.form.get("text_input", "").strip()
    file = request.files.get("file")
    if not text and not file:
        return jsonify({"ok": False, "error": "Provide text or upload a file."}), 400

    result = {}
    if text:
        result["text_prediction"] = predict_from_text(text)

    if file:
        filename = secure_filename(file.filename or "upload.bin")
        if not allowed(filename):
            return jsonify({"ok": False, "error": "File type not allowed."}), 400
        path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(path)
        with open(path, "rb") as f:
            blob = f.read()
        result["file_prediction"] = predict_from_bytes(blob, filename)

    result["confidence"] = round(random.uniform(0.6, 0.98), 2)
    result["processed_at"] = int(time.time())
    return jsonify({"ok": True, "result": result})

# Backward-compatible route: /predict behaves the same as /api/predict
@app.route("/predict", methods=["POST"])
def predict_compat():
    return api_predict()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
