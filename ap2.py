import requests
import time
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///enderecos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Enderecos(db.Model):
    cep = db.Column(db.String(8), primary_key=True)
    logradouro = db.Column(db.String(100))
    complemento = db.Column(db.String(100))
    bairro = db.Column(db.String(100))
    localidade = db.Column(db.String(100))
    uf = db.Column(db.String(2))
    ibge = db.Column(db.String(20))
    gia = db.Column(db.String(10))
    ddd = db.Column(db.String(10))
    siafi = db.Column(db.String(10))

def pesquisar_e_salvar_endereco(cep):
    url = f'https://viacep.com.br/ws/{cep}/json/'
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        dados_endereco = resposta.json()
        print(dados_endereco)
        
        if 'erro' not in dados_endereco:
            with app.app_context():
                enderecos = Enderecos(
                    cep=dados_endereco.get('cep', 'N/A').replace('-', ''),
                    logradouro=dados_endereco.get('logradouro', 'N/A'),
                    complemento=dados_endereco.get('complemento', 'N/A'),
                    bairro=dados_endereco.get('bairro', 'N/A'),
                    localidade=dados_endereco.get('localidade', 'N/A'),
                    uf=dados_endereco.get('uf', 'N/A'),
                    ibge=dados_endereco.get('ibge', 'N/A'),
                    gia=dados_endereco.get('gia', 'N/A'),
                    ddd=dados_endereco.get('ddd', 'N/A'),
                    siafi=dados_endereco.get('siafi', 'N/A')
                )
                db.session.add(enderecos)
                db.session.commit()
                print(f"Endereço salvo: {dados_endereco}")
        else:
            print('CEP não encontrado')
    except requests.RequestException as e:
        print(f"Erro ao consultar a API: {e}")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    while True:
        cep = input("Digite o CEP que deseja pesquisar (ou digite 'sair' para sair): ")
        if cep.lower() == 'sair':
            break
        pesquisar_e_salvar_endereco(cep)

    time.sleep(5)