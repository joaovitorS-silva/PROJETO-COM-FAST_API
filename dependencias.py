
from fastapi import Depends , HTTPException
from modelos import bd, Usuarios
from sqlalchemy.orm import sessionmaker, Session
from pwdlib import PasswordHash
from jose import jwt , JWTError # O JWTERROR DISPARA PARA ERROS DE AUTENTICAÇÃO OU EXPIRAÇÃO (TOKEN)
from main import SECRET_KEY, ALGORITHM, oauth2_schema

password_hash = PasswordHash.recommended()

def pegar_sessao():
    try:
        Session = sessionmaker(bind=bd)
        session = Session()
        yield session # o yield faz com que a funcao pare e envie a sessao para a chamada
    finally:
        session.close()


def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    #verificaçao de token:
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = int(dic_info.get("sub"))
        tipo = (dic_info.get("type"))
    except JWTError:
        raise HTTPException(status_code=401, detail="acesso negado, verifique a validade")
    #verificar se ele estar usando o acces token
    tipo = (dic_info.get("type"))
    if tipo != "access":
            raise HTTPException(status_code=401, detail="use o access token, nao o refresh token")
    
    usuario = session.query(Usuarios).filter(Usuarios.id==id_usuario).first() 
    if not usuario:
        raise HTTPException (status_code=401, detail="acesso invalido")
    return usuario


def verificar_refresh_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    #verificaçao de token:
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = int(dic_info.get("sub"))
        tipo = (dic_info.get("type"))
    except JWTError:
        raise HTTPException(status_code=401, detail="acesso negado, verifique a validade")
    
    if tipo != "refresh": #verifica se é refresh
            raise HTTPException(status_code=401, detail="use o refresh token, nao o access token")
    
    usuario = session.query(Usuarios).filter(Usuarios.id==id_usuario).first() 
    if not usuario:
        raise HTTPException (status_code=401, detail="acesso invalido")
    return usuario