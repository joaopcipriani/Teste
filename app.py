from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, jsonify
import os
import time
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Caminho absoluto para uploads dentro do container
UPLOAD_FOLDER = "/app/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Função para salvar metadados
def save_metadata(filename, original_ctime=None):
    meta_path = os.path.join(app.config["UPLOAD_FOLDER"], filename + ".meta.json")
    meta = {
        "original_ctime": original_ctime if original_ctime else time.time()
    }
    with open(meta_path, "w") as f:
        json.dump(meta, f)

# Função para ler metadados
def read_metadata(filename):
    meta_path = os.path.join(app.config["UPLOAD_FOLDER"], filename + ".meta.json")
    if os.path.exists(meta_path):
        with open(meta_path, "r") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

# Página inicial
@app.route("/")
def index():
    return render_template("index.html")

# Upload de arquivos
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        flash("Nenhum arquivo enviado.")
        return redirect(url_for("index"))
    file = request.files["file"]
    if file.filename == "":
        flash("Nome de arquivo inválido.")
        return redirect(url_for("index"))

    filename = secure_filename(file.filename)
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    # Evita conflito com nomes duplicados
    base, ext = os.path.splitext(filename)
    counter = 1
    while os.path.exists(save_path):
        filename = f"{base}_{counter}{ext}"
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        counter += 1

    file.save(save_path)

    # Tenta preservar a data original se enviada pelo cliente (opcional)
    original_ctime = request.form.get("original_ctime")
    if original_ctime:
        try:
            original_ctime = float(original_ctime)
        except:
            original_ctime = time.time()
    else:
        original_ctime = time.time()

    save_metadata(filename, original_ctime)
    flash(f"Arquivo {filename} enviado com sucesso!")
    return redirect(url_for("index"))

# Download
@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)

# Delete
@app.route("/delete/<filename>", methods=["DELETE", "GET"])
def delete_file(filename):
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    meta_path = path + ".meta.json"
    if os.path.exists(path):
        os.remove(path)
        if os.path.exists(meta_path):
            os.remove(meta_path)
        return jsonify({"ok": True})
    return jsonify({"error": "Arquivo não encontrado"}), 404

# JSON para frontend moderno
@app.route("/files_json")
def files_json():
    try:
        files = []
        for f in os.listdir(app.config["UPLOAD_FOLDER"]):
            if f.endswith(".meta.json"):
                continue  # ignora arquivos de metadados
            path = os.path.join(app.config["UPLOAD_FOLDER"], f)
            stat = os.stat(path)
            meta = read_metadata(f)
            original_ctime = meta.get("original_ctime", stat.st_ctime)
            files.append({
                "name": f,
                "size": stat.st_size,
                "ctime": original_ctime,      # data original
                "mtime": stat.st_mtime         # data de modificação real
            })
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
