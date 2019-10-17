from flask import Flask, jsonify, request, render_template
import requests as Req

app = Flask(__name__)

@app.route('/')
def all():
    alunos = Req.get("http://localhost:5001/alunos").json()
    professores = Req.get("http://localhost:5002/professores").json()
    disciplinas = Req.get("http://localhost:5003/disciplinas").json()
    return render_template("index.html", alunos=alunos, professores=professores, disciplinas=disciplinas)

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
