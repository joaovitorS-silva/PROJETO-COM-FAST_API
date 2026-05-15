from sqlalchemy import create_engine , Integer, Boolean, Float, String, ForeignKey, Column
from sqlalchemy import declarative_base
bd = create_engine("slqite://banco.db")

#cria base do banco, meio q ela pega classe do python e "traduz para uma tabela"
base = declarative_base()

#classes da tabelas
class Usuarios(base)
    __tablename__ = "Usuarios"

    id = Column("identificador" ,Integer, primary_key=True, autoincrement=True)
    nome = Column("nome usuario", String,)
    email = Column("email" ,String , nullable=False)
    senha =Column("senha" ,String ,)
    numero =Column("telefone" ,String)
    adm = Column("adiminstrador", Boolean, default=False)
    ativo =Column("ativo" ,Boolean)

    def __init__(self,nome, email, senha, numero, ativo=True, adm= False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.numero = numero
        self.ativo = ativo
        self.adm = adm

#pedidos

class Pedidos(base)
    __tablename__ = "pedidos"

    id = Column("identificador", Integer, primary_key=True, autoincrement=True)
    numero_pedido =Column("numero do pedido", Integer, nullable=False)
    valor = Column("valor do pedido", Float, nullable=False)
    numero_telefone = Column ("telefone", String)
    pass

#itens do pedido