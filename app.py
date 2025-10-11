from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Caminho absoluto dentro do container (docker-compose mapeia /home/joao/... para /app/uploads)
UPLOAD_FOLDER = "/app/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Rota principal - mostra a página HTML
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
    flash(f"Arquivo {filename} enviado com sucesso!")
    return redirect(url_for("index"))

# Download de arquivos
@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)

# Apagar arquivos
@app.route("/delete/<filename>", methods=["DELETE", "GET"])
def delete_file(filename):
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    if os.path.exists(path):
        os.remove(path)
        flash(f"Arquivo {filename} removido.")
        return jsonify({"ok": True})
    else:
        flash(f"Arquivo {filename} não encontrado.")
        return jsonify({"error": "Arquivo não encontrado"}), 404

# Endpoint JSON para frontend moderno
@app.route("/files_json")
def files_json():
    try:
        files = []
        for f in os.listdir(app.config["UPLOAD_FOLDER"]):
            path = os.path.join(app.config["UPLOAD_FOLDER"], f)
            stat = os.stat(path)
            files.append({
                "name": f,
                "size": stat.st_size,
                "ctime": stat.st_ctime,
                "mtime": stat.st_mtime
            })
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
