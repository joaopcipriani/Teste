import os
from flask import Flask, request, jsonify, send_from_directory, render_template

app = Flask(__name__)
UPLOAD_FOLDER = '/app/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_unique_filename(filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    new_name = filename
    while os.path.exists(os.path.join(UPLOAD_FOLDER, new_name)):
        new_name = f"{base}_{counter}{ext}"
        counter += 1
    return new_name

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if not file:
        return 'Nenhum arquivo', 400
    safe_name = file.filename.replace('/', '_')
    unique_name = get_unique_filename(safe_name)
    file.save(os.path.join(UPLOAD_FOLDER, unique_name))
    return jsonify({'ok': True, 'filename': unique_name})

@app.route('/files')
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    file_info = []
    for f in files:
        path = os.path.join(UPLOAD_FOLDER, f)
        stat = os.stat(path)
        file_info.append({
            'name': f,
            'size': stat.st_size,
            'mtime': stat.st_mtime
        })
    return jsonify(file_info)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@app.route('/delete/<filename>', methods=['DELETE'])
def delete(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(path):
        os.remove(path)
        return jsonify({'ok': True})
    return 'Arquivo não encontrado', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
