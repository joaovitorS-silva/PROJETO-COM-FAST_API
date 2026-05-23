from sqlalchemy import create_engine , Integer, Boolean, Float, String, ForeignKey, Column
from sqlalchemy.orm import declarative_base , relationship   




bd = create_engine("mysql+pymysql://root:1234@localhost/bd_pedidos")

#cria base do banco, meio q ela pega classe do python e "traduz para uma tabela"
base = declarative_base()

#classes da tabelas
class Usuarios(base):
    __tablename__ = "usuarios"

    id = Column("id" ,Integer, primary_key=True, autoincrement=True) #id_usuario
    nome = Column("nome", String(255))
    email = Column("email" ,String(50))
    senha =Column("senha" ,String (60))
    numero =Column("telefone" ,String(60))
    adm = Column("adiminstrador", Boolean, default=False)
    ativo =Column("ativo" ,Boolean)

    def __init__(self,nome, email, senha, numero, ativo=True,adm=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.numero = numero
        self.ativo = ativo
        self.adm = adm

#pedidos

class Pedido(base):
    __tablename__ = "pedidos"
    id = Column("id", Integer, primary_key=True, autoincrement=True) #id_pedidom, la em itens
    status = Column("status", String(50))
    id_usuario = Column("usuario", ForeignKey("usuarios.id"))
    preco = Column("valor_do_pedido", Float)
    itens = relationship("ItemPedido", cascade = "all , delete")

    def __init__(self, usuario, preco=0, status="PENDENTE"):
        self.id_usuario = usuario   
        self.status = status
        self.preco = preco
        
    def calcular_preco(self):
        preco_pedido = 0
        for item in self.itens:
            preco_item = item.preco_unitario * item.quantidade # nao entendi essa linha (entender ela no final)
            preco_pedido += preco_item
        self.preco = preco_pedido
        return preco_pedido
    
    #itens do pedido
class ItemPedido(base):
    __tablename__ = ("itens_pedido")

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    tamanho = Column("tamanho", String(60))
    quantidade = Column("quantidade", Integer)
    sabor = Column("sabor", String(60))
    preco_unitario = Column("preco_unitario", Float)
    id_pedido = Column("numero_pedido", ForeignKey("pedidos.id")) #id_pedido

    def __init__(self, tamanho,quantidade, sabor, preco_unitario, pedido):
        self.tamanho = tamanho
        self.quantidade = quantidade
        self.sabor = sabor
        self.preco_unitario = preco_unitario
        self.pedido = pedido
      
        

