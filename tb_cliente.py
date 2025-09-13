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
    
    return gera_resposta(200, "Lista de Clientes", cliente_json, "Uhu, Clientes Retornados!")

#MÉTODO 2 - GET (POR ID)
@app.route("/clientes/<id_cliente_pam>", methods=["GET"])
def seleciona_cliente_by_id(id_cliente_pam):
    cliente_selecionado = ClinicaVet.query.filter_by(id_cliente = id_cliente_pam).first()
    cliente_json = cliente_selecionado.to_json()

    return gera_resposta(200, "Lista de Clientes", cliente_json, 'Eba, Cliente Encontrado!')


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
        return gera_resposta(201, "Lista de Clientes", cliente.to_json(), 'Opa, cadastro criado com sucesso!')

    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, "Lista de Clientes", {}, 'Ihhh, Erro ao Cadastrar Cliente')        


# MÉTODO 4 - PUT (ATUALIZAR)

@app.route("/clientes/<id_cliente_adiciona>", methods=["PUT"])
def atualiza_cliente(id_cliente_adiciona):
    adiciona_cliente = ClinicaVet.query.filter_by(id_cliente = id_cliente_adiciona).first()
    body = request.get_json()

    try:
        if('nome' in body):
            adiciona_cliente.nome = body['nome']
        if('endereco' in body):
            adiciona_cliente.endereco = body['endereco']
        if('telefone' in body):
            adiciona_cliente.telefone = body['telefone']

        mybd.session.add(adiciona_cliente)
        mybd.session.commit()
        
        return gera_resposta(200, "Lista de Clientes", adiciona_cliente.to_json(), "Olha Lá, Cliente Adicionado com Sucesso!")
    except Exception as e:
        print('Eita, Deu Erro!', e)
        return gera_resposta(400, "Lista de Clientes", {}, "Caramba, Erro ao Atualizar Banco de Dados")
    
# MÉTODO 5 - DELETE (APAGAR)
@app.route("/clientes/<id_cliente_deleta>", methods=["DELETE"])
def deleta_cliente(id_cliente_deleta):
    deleta_cliente = ClinicaVet.query.filter_by(id_cliente = id_cliente_deleta).first()

    try:
        mybd.session.delete(deleta_cliente)
        mybd.session.commit()
        return gera_resposta(200, deleta_cliente.to_json(), "Vish, Cliente Deletado!")
    except Exception as e:
        print("Eita, Deu Erro!")
        return gera_resposta(400, "Lista de Clientes", {}, "Rapaz, Errou Rude!")

#-------------------------------------------

class Pet(mybd.Model):
    __tablename__ = 'tb_pets'
    id_pet = mybd.Column(mybd.Integer, primary_key=True, autoincrement=True)
    nome = mybd.Column(mybd.String(255))
    tipo = mybd.Column(mybd.String(255))
    raca = mybd.Column(mybd.String(255))
    data_nascimento = mybd.Column(mybd.String(255)) # ou db.Date
    id_cliente = mybd.Column(mybd.Integer, mybd.ForeignKey('tb_pets.id_pet'), nullable=False)

    def to_json(self):
        return {
            "id_pet": self.id_pet,
            "nome": self.nome,
            "tipo": self.tipo,
            "raca": self.raca,
            "data_nascimento": str(self.data_nascimento),
            "id_cliente": self.id_cliente
        }

# MÉTODO 1 - GET (CONSULTA)
@app.route("/pets", methods=["GET"])
def seleciona_pet():
    pet_selecionado = Pet.query.all()
    pet_json = [pet.to_json()
                for pet in pet_selecionado]
    return gera_resposta(200, "Lista de Pets", pet_json, 'Uhu, Pets Retornados!')


# MÉTODO 2 - GET POR ID (CONSULTA POR ID))
@app.route("/pets/<id_pet_pam>", methods=["GET"])
def seleciona_pet_by_id(id_pet_pam):
    pet_selecionado = Pet.query.filter_by(id_pet = id_pet_pam).first()
    pet_json = pet_selecionado.to_json()

    return gera_resposta(200, "Lista de Pets", pet_json, 'Eba, Pet Encontrado!')


# MÉTODO 3 - POST (ACRESCENTAR)
@app.route("/pet", methods=["POST"])
def criar_pet():
    requisicao = request.get_json()

    try:
        pet = Pet(
            id_pet = requisicao['id_pet'],
            nome = requisicao['nome'],
            tipo = requisicao['tipo'],
            raca = requisicao['raca'],
            data_nascimento = requisicao['data_nascimento'],
            id_cliente = requisicao['id_cliente']
        )

        mybd.session.add(pet)
        mybd.session.commit()
        return gera_resposta(201, "Lista de Pets", pet.to_json(), 'Opa, Cadastro Criado com Sucesso!')
    
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, "Lista de Pets", {}, 'Eita, Erro ao Cadastar Pet!')

# MÉTODO 4 - PUT
@app.route("/pet/<id_pet_adiciona>", methods=["PUT"])
def atualizada_pet(id_pet_adiciona):
    adiciona_pet = Pet.query.filter_by(id_pet = id_pet_adiciona).first()
    body = request.get_json()

    try:
        if('nome' in body):
            adiciona_pet.nome = body['nome']
        if('tipo' in body):
            adiciona_pet.tipo = body['tipo']
        if('raca' in body):
            adiciona_pet.tipo = body['raca']
        if('data_nascimento' in body):
            adiciona_pet.data_nascimento = body['data_nascimento']

        mybd.session.add(adiciona_pet)
        mybd.session.commit()

        return gera_resposta(200, "Lista de Pets", adiciona_pet.to_json(), "Olha Lá, Pet Adicionado com Sucesso!")
    except Exception as e:
        print('Eita, Deu Erro!')
        return gera_resposta(400, "Lista de Pets", {}, "Caramba, Erro ao Atualizar Banco de Dados!")

# MÉTODO 5 - DELETE (APAGAR)
@app.route("/pet/<id_pet_deleta>", methods=["DELETE"])
def deleta_pet(id_pet_deleta):
    deleta_pet = Pet.query.filter_by(id_pet = id_pet_deleta).first()

    try:
        mybd.session.delete(deleta_pet)
        mybd.session.commit()
        return gera_resposta(200, deleta_pet.to_json(), "Vish, Pet Deletado !")
    except Exception as e:
        print("Eita, Deu Erro!")
        return gera_resposta(400, "Lista de Pets", {}, "Rapaz, Errou Rude!")


# ------------------------------------------
# RESPOSTA PADRÃO
def gera_resposta(status, titulo, conteudo, mensagem=False):
    body = {}
    body[titulo] = conteudo

    if(mensagem):
        body['Mensagem'] = mensagem
    
    return Response(json.dumps(body), status = status, mimetype = 'application/json')

app.run(port=5000, host='localhost', debug=True)


