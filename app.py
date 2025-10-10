from flask import Flask, request, render_template_string

app = Flask(__name__)

# HTML simples embutido no código
HTML_FORM = """
<!doctype html>
<title>Teste Oi</title>
<h2>Digite "Oi"</h2>
<form method="post">
  <input name="mensagem" type="text">
  <input type="submit" value="Enviar">
</form>
{% if resposta %}
  <p><strong>{{ resposta }}</strong></p>
{% endif %}
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    resposta = None
    if request.method == 'POST':
        mensagem = request.form.get('mensagem', '')
        if mensagem == "Oi":
            resposta = "Oi OK"
        else:
            resposta = "Não entendi"
    return render_template_string(HTML_FORM, resposta=resposta)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

