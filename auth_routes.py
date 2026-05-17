from fastapi import APIRouter, Depends , HTTPException
from modelos import Usuarios
from dependencias import pegar_sessao , password_hash
from schemas import UsuarioSchema, LoginSchemas
from sqlalchemy.orm import Session
from jose import JWTError , jwt
from datetime import datetime, timezone, timedelta
from main import ACCES_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM


auth_router = APIRouter(prefix="/auth", tags=["autenticaçao"])

#token de acesso pois, toda vez que um usuario logar vai receber
#  token e reutilizae em outros endpoints
def criar_token(id_usuario):
    data_expiracao = datetime.now(timezone.utc) + timedelta(minutes=ACCES_TOKEN_EXPIRE_MINUTES)
    dict_info = {"sub": id_usuario,
                  "exp": data_expiracao
                  }
    jwt_codificado = jwt.encode(dict_info, SECRET_KEY, ALGORITHM)
    return jwt_codificado


def verificar_login(senha, email, session):
    usuario = session.query(Usuarios).filter(Usuarios.email==email).first()
    if not usuario:
        return False
    elif not password_hash.verify(senha, usuario.senha):
        return False

    return usuario

@auth_router.get("/")
async def home():
    """
    essa é rota padrão de autenticação  do nosso sistema
    """
    return{"mensagem": "vc estar autenticado", "autenticado": False}


@auth_router.post("/criar_usuario")
async def criar(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)): #estrutura de tipagem de schemas para ficar mais rapido na execução
    usuario = session.query(Usuarios).filter(Usuarios.email==usuario_schema.email).first()
    if usuario:

        raise HTTPException(status_code=404, detail="usuario ja cadastrado" ) 
    else:

        senha_criptografada = password_hash.hash(usuario_schema.senha)
        novo_usuario = Usuarios( usuario_schema.nome, usuario_schema.email, senha_criptografada,  usuario_schema.numero)
        session.add(novo_usuario)
        session.commit()
        return{"mensagem": f"novo usuario cadastrado com sucesso {usuario_schema.email}"}
    

@auth_router.post("/login")
async def login(login_schema: LoginSchemas, session: Session = Depends(pegar_sessao)):
    usuario = verificar_login(login_schema.senha, login_schema.email, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="usuario nao encontrado ou credencias e icorretas")
    else:
        access_token = criar_token(usuario.id)
        return{
            "acess_token": access_token,
            "token_type": "bearer"
        }
