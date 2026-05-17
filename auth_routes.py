from fastapi import APIRouter, Depends
from modelos import Usuarios
from dependencias import pegar_sessao , password_hash


auth_router = APIRouter(prefix="/auth", tags=["autenticaçao"])

@auth_router.get("/")
async def home():
    """
    essa é rota padrão de autenticação  do nosso sistema
    """
    return{"mensagem": "vc estar autenticado", "autenticado": False}
@auth_router.post("/criar_usuario")
async def criar(email : str, senha:str, nome:str, numero:str, session=Depends(pegar_sessao)):
    usuario = session.query(Usuarios).filter(Usuarios.email==email).first()
    if usuario:
            #tem um problema aqui pois isso era pra ser um erro e nao uma mensagem 200 de (sucesso)
        return {"mensagem": "ja existe um usuario cadastrado"}
    else:
   
   
        senha_criptografada = password_hash.hash(senha)
        novo_usuario = Usuarios( nome, email, senha_criptografada, numero)
        session.add(novo_usuario)
        session.commit()
        return{"mensagem": "novo ususario cadastrado com sucesso"}