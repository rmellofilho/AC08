from flask import Flask, jsonify, request, render_template
from services.disciplinas_service import \
    listar as service_listar, \
    localizar as service_localizar, \
    criar as service_criar, \
    remover as service_remover, \
    atualizar as service_atualiza, \
    resetar as service_resetar, \
    cadastrar_aluno as service_cadastrar_aluno, \
    remover_aluno as service_remover_aluno, \
    consultar_alunos as service_consultar_alunos
       
import requests as Req
import infra.disciplinas_db as disciplinas_db
import infra.disciplinas_alunos_db as disciplinas_alunos_db

disciplinas_db.init()
disciplinas_alunos_db.init()

msg_cadastrar = "Entre com o ID da disciplina e do aluno para Cadastrar um aluno a uma disciplina."
msg_remover = "Entre com o ID da disciplina para remove-la."
msg_aluno_cadastar = "Entre com o id da disciplina e do aluno para cadastra-lo em uma disciplina!"
msg_aluno_remover = "Entre com o id da disciplina e do aluno para remove-lo em uma disciplina!"
msg_aluno_listar = "Lista de alunos por disciplina."

disciplinas_app = Flask(__name__)
disciplinas_app.debug = True

def listar_alunos():
    return Req.get('http://localhost:5001/alunos').json()

def renderizar_pagina(disciplina='', alunos_disciplina='', msg_cadastrar_pre='', msg_remover_pre='', msg_aluno_cadastar_pre='', msg_aluno_remover_pre='', msg_aluno_listar_pre=msg_aluno_listar):
    alunos = listar_alunos()
    return render_template( \
        "index.html", \
        disciplinas=service_listar(), \
        disciplina=disciplina, \
        alunos=alunos if alunos != None else [], \
        alunos_disciplina = alunos_disciplina)

    
@disciplinas_app.route('/disciplinas')
def listar_disciplinas():
    lista = service_listar()
    return jsonify(lista)

@disciplinas_app.route('/disciplinas', methods=['POST'])
def cadastrar_disciplina():
    nova_disciplina = request.get_json()
    if "nome" not in nova_disciplina:
        return jsonify({'erro':'disciplina sem nome'}), 400
    disciplina = service_criar(nova_disciplina)
    if disciplina == None:
        return jsonify({'erro':'disciplina ja existe'}), 400
    return jsonify(disciplina)
    
@disciplinas_app.route('/site/disciplinas', methods=['POST'])
def cadastrar_disciplina_site():
    nova_disciplina = request.get_json()
    if "nome" not in nova_disciplina:
        return jsonify({'erro':'disciplina sem nome'}), 400
    disciplina = service_criar(nova_disciplina)
    if disciplina == None:
        return renderizar_pagina(msg_cadastrar_pre="Disciplina não pôde ser cadastrada! "), 400
	return renderizar_pagina()
    # return jsonify(disciplina)

@disciplinas_app.route('/disciplinas/<int:id>', methods=['PUT'])
def alterar_disciplina(id):
    disciplina_data = request.get_json()
    if ('nome' not in disciplina_data):
        return jsonify({'erro':'disciplina sem nome'}), 400
    if ('professor' not in disciplina_data):
        return jsonify({'erro':'disciplina sem professor'}), 400
    # atualizado = service_atualiza(id, disciplina_data['nome'], disciplina_data['professor_id'],disciplina_data['alunos'])
    atualizado = service_atualiza(id, disciplina_data['nome'], disciplina_data['professor_id'])
    if atualizado != None:
        return jsonify(atualizado), 200
    return jsonify({'erro':'Disciplina nao encontrado'}), 400
    
@disciplinas_app.route('/disciplinas/<int:id>', methods=['GET'])
def localizar_disciplina(id):
    disciplina = service_localizar(id)
    if disciplina != None:
        return jsonify(disciplina)
    return jsonify({'erro':'disciplina nao encontrado'}), 400

@disciplinas_app.route('/disciplinas/<int:id>', methods=['DELETE'])
def remover_disciplina(id):
	removido = service_remover(id)
    if removido == 1:
        return jsonify(removido), 202
    return jsonify({'erro':'disciplina nao encontrado'}), 400

@disciplinas_app.route('/site/disciplinas/delete', methods=['POST'])
def remover_disciplina_site():
    id = request.form["id"]
    if id == None:
        return render_template("index.html", disciplinas=service_listar(), mensagem = msg_cadastrar,msg_remover="Informe um Id válido para remover uma disciplina! " + msg_remover)
    removido = service_remover(id)
    if removido == 1:
        return jsonify(removido), 202

@disciplinas_app.route('/disciplinas/resetar', methods=['DELETE'])
def resetar():
    service_resetar()
    return jsonify("Base de disciplinas reiniciada"), 202

@disciplinas_app.route('/')
def all():
    return renderizar_pagina()

#Feito
@disciplinas_app.route('/disciplinas/<int:disciplina_id>/alunos/listar', methods=['GET'])
def listar_alunos_por_disciplina(disciplina_id):
    id = request.form["id"]
    if id == None:
        return render_template("index.html", disciplinas=service_listar(), mensagem = msg_cadastrar,msg_remover="Informe um Id válido para remover uma disciplina! " + msg_remover)
    alunos_por_disciplina = service_listar(disciplina_id)
    if alunos_por_disciplina != None:
        return render_template("index.html", disciplinas(service_listar())
    return jsonify({'erro':'Nenhum aluno por disciplina encontrado.'}), 400

#Feito
@disciplinas_app.route('/site/disciplinas/alunos/listar', methods=['POST'])
def listar_alunos_por_disciplina_site():
    disciplina_id = request.form["disciplinaid"]
    if disciplina_id == None:
        return jsonify('erro': 'Não foi possivel listar aluno por disciplina.')
    alunos_por_disciplina_site = service_listar(disciplina_id)
    if alunos_por_disciplina_site != None:
        return render_template("index.html", disciplinas(service_listar())


#FEITO
@disciplinas_app.route('/disciplinas/alunos', methods=['POST'])
def cadastrar_aluno_por_disciplina():
    dados = request.get_json()
    if dados == None:
        return jsonify({'erro':'dados não informados corretamente','dados':dados}), 400
    aluno = service_cadastrar_aluno(dados)
    if aluno == None:
        return jsonify({'erro':'aluno já cadastrado'}), 400
    return jsonify(aluno)


#Feito
@disciplinas_app.route('/site/disciplinas/alunos', methods=['POST'])
def cadastar_aluno_por_disciplina_site():
    disciplina_id = request.form["disciplinaid"]
    aluno_id = request.form["alunoid"]
    if disciplina_id == None:
        return jsonify({'erro':msg_aluno_cadastar})
    if aluno_id == None:
        return jsonify({'erro':msg_aluno_cadastar})
    cadastro = service_cadastrar_aluno(dados)
    if cadastro == None:
        return jsonify({'erro':"Aluno não pôde ser cadastrado!"})
    return render_template("index.html", service_listar())

#Feito
@disciplinas_app.route('/disciplinas/<int:disciplina_id>/alunos/<int:aluno_id>', methods=['DELETE'])
def remover_aluno_por_disciplina(disciplina_id, aluno_id):
    idDisciplina = disciplina_id
    idAluno = aluno_id
    if idDisciplina != None and idAluno != None:
        remove_aluno = service_remover(idAluno, idDisciplina)
        return jsonify(remove_aluno), 200

#Feito
@disciplinas_app.route('/site/disciplinas/alunos/delete', methods=['POST'])
def remover_aluno_por_disciplina_site():
    disciplina_id = request.form["disciplinaid"]
     if disciplina_id != None:
        disciplina_remove = service_remover(disciplina_id)
        return jsonify(disciplina_remove), 200
    
if __name__ == '__main__':
    disciplinas_app.run(host='localhost', port=5003)
