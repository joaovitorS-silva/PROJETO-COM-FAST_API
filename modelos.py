from sqlalchemy import create_engine , Integer, Boolean, Float, String, ForeignKey, Column
from sqlalchemy.orm import declarative_base   


#from sqlalchemy.types import ChoiceType

bd = create_engine("sqlite:///banco.db")

#cria base do banco, meio q ela pega classe do python e "traduz para uma tabela"
base = declarative_base()

#classes da tabelas
class Usuarios(base):
    __tablename__ = "usuarios"

    id = Column("id" ,Integer, primary_key=True, autoincrement=True)
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

class Pedido(base):
    __tablename__ = "pedidos"
    #status_do_pedido = (
        
        #BANCO     E   USUARIO(MSG)
      #  ("PENDENTE", "PENDENTE")
       # ("CONCLUIDO", "CONCLUIDO")
       # ("CANCELADO", "CANCELADO")              ======nao vou usar isso agora pois a migraçao  para 
       #                                               o banco de dados nao fica automatica dar erro 
       #                                                               com o alembic===========
    #)
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String)
    usuario = Column("usuario", ForeignKey("usuarios.id"))
    #itens = 
    preco = Column("valor do pedido", Float)

    def __init__(self, usuario, preco, status="PENDENTE"):
        self.usuario = usuario
        self.status = status
        self.preco = preco
        
    
    #itens do pedido
class itenspedido(base):
    __tablename__ = ("itens_pedido")
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    tamanho = Column("tamanho", String)
    sabor = Column("sabor", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido = Column("numero_pedido", ForeignKey("pedidos.id"))

    def __init__(self, tamanho, sabor, preco_unitario, pedido):
        self.tamanho = tamanho
        self.sabor = sabor
        self.preco_unitario = preco_unitario
        self.pedido = pedido

        

