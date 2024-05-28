import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String

engine = create_engine('sqlite:///enderecos.db')

Session = sessionmaker(bind=engine)

session = Session()

Base = declarative_base()

class Endereco(Base):
    __tablename__ = 'Enderecos'
    cep = Column(String, primary_key=True)
    logradouro = Column(String)
    complemento = Column(String)
    bairro = Column(String)
    localidade = Column(String)
    uf = Column(String)
    ibge = Column(String)
    gia = Column(String)
    ddd = Column(String)
    siafi = Column(String)

Base.metadata.create_all(engine)

def consultar_e_inserir_endereco(cep):
    url = f'https://viacep.com.br/ws/{cep}/json/'
    resposta = requests.get(url)
    if resposta.status_code == 200:
        data = resposta.json()
        
#Verifica se o CEP já existe no banco de dados
        endereco_existente = session.query(Endereco).filter_by(cep=cep).first()
        if endereco_existente:
            print("O endereço com o CEP", cep, "já existe no banco de dados. Pulando para o próximo CEP...")
            return
            
        endereco = Endereco(cep=data['cep'],
                            logradouro=data['logradouro'],
                            complemento=data['complemento'],
                            bairro=data['bairro'],
                            localidade=data['localidade'],
                            uf=data['uf'],
                            ibge=data['ibge'],
                            gia=data['gia'],
                            ddd=data['ddd'],
                            siafi=data['siafi'])
        session.add(endereco)
        try:
            session.commit()
            print("Endereço inserido com sucesso!")
        except Exception as e:
            session.rollback()  # Desfaz a transação para evitar o erro
            print("Erro ao inserir endereço:", e)
    else:
        print("Erro ao consultar o CEP:", resposta.status_code)

consultar_e_inserir_endereco('04013000')
consultar_e_inserir_endereco('01001000')