# Realizar um CRUD com a base de dados Clinica Vet (tb_cliente)

from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask("ClinicaVetBD")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Senai%40134@127.0.0.1/ClinicaVetBD'
mybd = SQLAlchemy(app)

class ClinicaVet(mybd.Model):
    __tablename__ = 'tb_clientes'
    id_cliente = mybd.Column(mybd.Integer, primary_key=True)
    nome = mybd.Column(mybd.String(255))
    endereco = mybd.Column(mybd.String(255))
    telefone = mybd.Column(mybd.String(255))

    def to_json(self):
        return{
            "id_cliente": self.id_cliente,
            "nome": self.nome,
            "endereco": self.endereco,
            "telefone": self.telefone
        }
# MÉTODO 1 - GET (CONSULTA)
@app.route("/clientes", methods=["GET"])
def seleciona_cliente():
    cliente_selecionado = ClinicaVet.query.all()
    cliente_json = [cliente.to_json()
                    for cliente in cliente_selecionado]
    
    return gera_resposta(200, cliente_json, "Uhu, Clientes Retornados!")

#MÉTODO 2 - GET (POR ID)
@app.route("/clientes/<id_cliente_pam>", methods=["GET"])
def seleciona_cliente_by_id(id_cliente_pam):
    cliente_selecionado = ClinicaVet.query.filter_by(id_cliente = id_cliente_pam).first()
    cliente_json = cliente_selecionado.to_json()

    return gera_resposta(200, cliente_json, 'Eba, Cliente Encontrado!')


# MÉTODO 3 - POST (CRIAR)
@app.route("/clientes", methods = ["POST"])
def criar_cliente():
    requisicao = request.get_json()
    
    try:
        cliente = ClinicaVet(
            id_cliente = requisicao['id_cliente'],
            nome = requisicao['nome'],
            endereco = requisicao['endereco'],
            telefone = requisicao['telefone']
        )

        mybd.session.add(cliente)
        mybd.session.commit()
        return gera_resposta(201, carro.to_json(), 'Opa, cadastro criado com sucesso!')

    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, {}, 'Ihhh, Erro ao Cadastrar Cliente')        


# MÉTODO 4 - PUT (atualizar)

@app.route("/clientes/<id_cliente>", methods=["PUT"])
def atualiza_cliente(id_cliente_adiciona):
    adiciona_cliente = ClinicaVet.query.filter_by(id_cliente = id_cliente_adiciona).first()
    body = request.get_json()

    try:
        if('nome' in body):
            adiciona_cliente.nome = body['marca']
        if('endereco' in body):
            adiciona_cliente.endereco = body['marca']
        if('telefone' in body):
            adiciona_cliente.telefone = body['telefone']

        mybd.session.add(adiciona_cliente)
        mybd.session.commit()
        
        return gera_resposta(200, "ClinicaVetDB", adiciona_cliente.to_json(), "Olha Lá, Cliente Adicionado com Sucesso!")
    except Exception as e:
        print('Eita, Deu Erro!')
        return gera_resposta(400, 'ClinicaVetDB', {}, "Caramba, Erro ao Atualizar Banco de Dados")
    
# MÉTODO 5 - DELETE (apagar)
@app.route("/clientes/<id_cliente>", methods=["DELETE"])
def deleta_cliente(id_cliente_deleta):
    deleta_cliente = ClinicaVet.query.filter_by(id_cliente = id_cliente_deleta).first()

    try:
        mybd.session.delete(deleta_cliente)
        mybd.session.commit()
        return gera_resposta(200, deleta_cliente.to_json(), "Vish, Cliente Deletado!")
    except Exception as e:
        print("Eita, Deu Erro!")
        return gera_resposta(400, "ClinicaVetDB", {}, "Rapaz, Errou Rude!")


# ------------------------------------------
# RESPOSTA PADRÃO
def gera_resposta(status, conteudo, mensagem=False):
    body = {}
    body['Lista de Clientes'] = conteudo

    if(mensagem):
        body['Mensagem'] = mensagem
    
    return Response(json.dumps(body), status = status, mimetype = 'application/json')

app.run(port=5000, host='localhost', debug=True)
