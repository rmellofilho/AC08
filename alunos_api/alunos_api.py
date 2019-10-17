from flask import Flask, jsonify, request, render_template
from services.alunos_service import \
    listar as service_listar, \
    localizar as service_localiza, \
    criar as service_criar, \
    remover as service_remover, \
    atualizar as service_atualiza, \
    resetar as service_resetar

import infra.alunos_db as alunos_db
alunos_db.init()

mensagem_inicial = "Entre com o Nome e Matrícula para cadastrar um aluno novo."
mensagem_remover = "Entre com o Id do aluno que deseja remover"

alunos_app = Flask(__name__)

def internal_cadastrar_aluno(dados_aluno):
    aluno = service_criar(dados_aluno)
    return aluno

@alunos_app.route('/alunos')
def listar_alunos():
    lista = service_listar()
    return jsonify(lista)

@alunos_app.route('/alunos', methods=['POST'])
def cadastrar_aluno():
    if request.form:
        novo_aluno = {"nome" :request.form["nome"], "matricula" : request.form["matricula"]}
    else:
        novo_aluno = request.get_json()
    if novo_aluno == None:
        return jsonify({'erro':'dados não informados corretamente:', 'dados':novo_aluno}), 400
    aluno = internal_cadastrar_aluno(novo_aluno)
    if aluno == None:
        return jsonify({'erro':'aluno ja existe'}), 400
    return jsonify(aluno)
    
@alunos_app.route('/site/alunos', methods=['POST'])
def cadastrar_aluno_site():
    if request.form["nome"] == None or request.form["matricula"] == None:
        return jsonify({'erro':'dados não informados corretamente:'}), 400
    novo_aluno = {"nome" :request.form["nome"], "matricula" : request.form["matricula"]}
    aluno = internal_cadastrar_aluno(novo_aluno)
    if aluno == None:
        return render_template("index.html", alunos=service_listar(), mensagem = "Aluno não pôde ser cadastrado! \n" + mensagem_inicial)
    return render_template("index.html", alunos=service_listar(), mensagem = mensagem_inicial)

@alunos_app.route('/alunos/<int:id>', methods=['PUT'])
def alterar_aluno(id):
    aluno_data = request.get_json()
    if ('nome' not in aluno_data):
        return jsonify({'erro':'aluno sem nome'}), 400
    if ('matricula' not in aluno_data):
        return jsonify({'erro':'aluno sem matricula'}), 400
    aluno_atualizado = service_atualiza(aluno_data)
    if aluno_atualizado != None:
        return jsonify(aluno_atualizado), 200
    return jsonify({'erro':'aluno nao foi atualizado'}), 400
    
@alunos_app.route('/alunos/<int:id>', methods=['GET'])
def localizar_aluno(id):
    aluno = service_localiza(id)
    if aluno != None:
        return jsonify(aluno)
    return jsonify({'erro':'aluno nao encontrado'}), 400

@alunos_app.route('/alunos/<int:id>', methods=['DELETE'])
def remover_aluno(id):
    removido = service_remover(id)
    if removido == 1:
        return jsonify(removido), 202
    return jsonify({'erro':'aluno nao encontrado'}), 400
    
@alunos_app.route('/site/alunos/delete', methods=['POST'])
def remover_aluno_site():
    id = request.form["id"]
    if id == None:
        return render_template("index.html", alunos=service_listar(), mensagem = mensagem_inicial,mensagem_remover="Informe um Id válido para remover um aluno! " + mensagem_remover)
    removido = service_remover(id)
    if removido == 1:
        return render_template("index.html", alunos=service_listar(), mensagem = mensagem_inicial,mensagem_remover="Aluno removido! " + mensagem_remover)
    return render_template("index.html", alunos=service_listar(), mensagem = mensagem_inicial,mensagem_remover=f"Não foi possível remover o aluno de id: {id}. {mensagem_remover}")

@alunos_app.route('/alunos/resetar', methods=['DELETE'])
def resetar():
    service_resetar()
    return jsonify("Base de alunos reiniciada"), 202

@alunos_app.route('/')
def all():
    return render_template("index.html", alunos=service_listar(), mensagem = mensagem_inicial,mensagem_remover=mensagem_remover)

if __name__ == '__main__':
    alunos_app.run(host='localhost', port=5001)
    