import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Configuração do Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///enderecos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização do SQLAlchemy e Flask-Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Modelo Endereco
class Endereco(db.Model):
    __tablename__ = 'Enderecos'
    cep = db.Column(db.String, primary_key=True)
    logradouro = db.Column(db.String)
    complemento = db.Column(db.String)
    bairro = db.Column(db.String)
    localidade = db.Column(db.String)
    uf = db.Column(db.String)
    ibge = db.Column(db.String)
    gia = db.Column(db.String)
    ddd = db.Column(db.String)
    siafi = db.Column(db.String)

# Função para consultar e inserir endereço
def consultar_e_inserir_endereco(cep):
    url = f'https://viacep.com.br/ws/{cep}/json/'
    resposta = requests.get(url)
    if resposta.status_code == 200:
        data = resposta.json()
        
        # Verifica se o CEP já existe no banco de dados
        endereco_existente = Endereco.query.filter_by(cep=cep).first()
        if endereco_existente:
            print(f"O endereço com o CEP {cep} já existe no banco de dados. Pulando para o próximo CEP...")
            return
        
        endereco = Endereco(
            cep=data['cep'],
            logradouro=data.get('logradouro', ''),
            complemento=data.get('complemento', ''),
            bairro=data.get('bairro', ''),
            localidade=data.get('localidade', ''),
            uf=data.get('uf', ''),
            ibge=data.get('ibge', ''),
            gia=data.get('gia', ''),
            ddd=data.get('ddd', ''),
            siafi=data.get('siafi', '')
        )
        db.session.add(endereco)
        try:
            db.session.commit()
            print("Endereço inserido com sucesso!")
        except Exception as e:
            db.session.rollback()  # Desfaz a transação para evitar o erro
            print("Erro ao inserir endereço:", e)
    else:
        print("Erro ao consultar o CEP:", resposta.status_code)

if __name__ == '__main__':
    with app.app_context():
        # Inicializa as tabelas no banco de dados (caso ainda não existam)
        db.create_all()
        consultar_e_inserir_endereco('04013000')
        consultar_e_inserir_endereco('01001000')
        consultar_e_inserir_endereco('05607000')
        consultar_e_inserir_endereco('01310200')
    app.run(debug=True)