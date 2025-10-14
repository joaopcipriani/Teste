from flask import Flask, request, render_template, jsonify
import os
import subprocess
import uuid

UPLOAD_FOLDER = "/tmp/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'dump' not in request.files:
        return "Nenhum arquivo enviado", 400
    file = request.files['dump']
    if file.filename == '':
        return "Arquivo vazio", 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], str(uuid.uuid4()) + "_" + file.filename)
    file.save(filepath)

    # Chamar análise do symreader-portable
    try:
        result = subprocess.run(
            ["dotnet", "symreader/symreader.dll", filepath],
            capture_output=True,
            text=True
        )
        output = result.stdout
        if result.returncode != 0:
            output += "\nErro: " + result.stderr
    except Exception as e:
        output = f"Erro ao executar análise: {e}"

    return jsonify({"analysis": output})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
