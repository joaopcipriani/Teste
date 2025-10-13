from flask import Flask, request, jsonify
from sym_translate import translate_address
import os

app = Flask(__name__)

@app.route("/translate", methods=["POST"])
def translate():
    data = request.json
    stack = data.get("stack", [])
    pid = os.getpid()  # só exemplo, ideal seria permitir escolher PID
    result = []
    for addr in stack:
        result.append(translate_address(pid, addr))
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
