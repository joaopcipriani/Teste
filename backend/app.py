from flask import Flask, request, jsonify
from sym_translate import translate_address_dummy

app = Flask(__name__)

@app.route("/translate", methods=["POST"])
def translate():
    data = request.json
    stack = data.get("stack", [])
    result = translate_address_dummy(stack)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
