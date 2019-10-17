from flask import Flask, jsonify, request, render_template
from services.professores_service import \
    listar as service_listar, \
    localizar as service_localiza, \
    criar as service_criar, \
    remover as service_remover, \
    atualizar as service_atualiza, \
    resetar as service_resetar

import infra.professores_db as professores_db
professores_db.init()

mensagem_inicial = "Entre com o Nome e RG para cadastrar um Professor novo."
mensagem_remover = "Entre com o Id do professor que deseja remover"

professores_app = Flask(__name__)

def internal_cadastrar_professor(dados_professor):
    professor = service_criar(dados_professor)
    return professor
    
@professores_app.route('/professores')
def listar_professores():
    lista = service_listar()
    return jsonify(lista)

@professores_app.route('/professores', methods=['POST'])
def cadastrar_professor():
    if request.form:
        novo_professor = {"nome" :request.form["nome"], "rg" : request.form["rg"]}
    else:
        novo_professor = request.get_json()
    if novo_professor == None:
        return jsonify({'erro':'dados não informados corretamente:', 'dados':novo_professor}), 400
    professor = internal_cadastrar_professor(novo_professor)
    if professor == None:
        return jsonify({'erro':'professor ja existe'}), 400
    return jsonify(professor)
    
@professores_app.route('/site/professores', methods=['POST'])
def cadastrar_professor_site():
    if request.form["nome"] == None or request.form["rg"] == None:
        return jsonify({'erro':'dados não informados corretamente:'}), 400
    novo_professor = {"nome" :request.form["nome"], "rg" : request.form["rg"]}
    professor = internal_cadastrar_professor(novo_professor)
    if professor == None:
        return render_template("index.html", professores=service_listar(), mensagem = "Professor não pôde ser cadastrado! \n" + mensagem_inicial)
    return render_template("index.html", professores=service_listar(), mensagem = mensagem_inicial)

@professores_app.route('/professores/<int:id>', methods=['PUT'])
def alterar_professor(id):
    professor_data = request.get_json()
    if ('nome' not in professor_data):
        return jsonify({'erro':'professor sem nome'}), 400
    if ('rg' not in professor_data):
        return jsonify({'erro':'professor sem rg'}), 400
    professor_atualizado = service_atualiza(professor_data)
    if professor_atualizado != None:
        return jsonify(professor_atualizado), 200
    return jsonify({'erro':'professor nao foi atualizado'}), 400
    
@professores_app.route('/professores/<int:id>', methods=['GET'])
def localizar_professor(id):
    professor = service_localiza(id)
    if professor != None:
        return jsonify(professor)
    return jsonify({'erro':'professor nao encontrado'}), 400

@professores_app.route('/professores/<int:id>', methods=['DELETE'])
def remover_professor(id):
    removido = service_remover(id)
    if removido == 1:
        return jsonify(removido), 202
    return jsonify({'erro':'professor nao encontrado'}), 400

@professores_app.route('/site/professores/delete', methods=['POST'])
def remover_professor_site():
    id = request.form["id"]
    if id == None:
        return render_template("index.html", professores=service_listar(), mensagem = mensagem_inicial,mensagem_remover="Informe um Id válido para remover um professor! " + mensagem_remover)
    removido = service_remover(id)
    if removido == 1:
        return render_template("index.html", professores=service_listar(), mensagem = mensagem_inicial,mensagem_remover="Professor removido! " + mensagem_remover)
    return render_template("index.html", professores=service_listar(), mensagem = mensagem_inicial,mensagem_remover=f"Não foi possível remover o professor de id: {id}. {mensagem_remover}")

@professores_app.route('/professores/resetar', methods=['DELETE'])
def resetar():
    service_resetar()
    return jsonify("Base de professores reiniciada"), 202

@professores_app.route('/')
def all():
    return render_template("index.html", professores=service_listar(), mensagem = mensagem_inicial)

if __name__ == '__main__':
    professores_app.run(host='localhost', port=5002)
    