
from fastapi import Depends , HTTPException
from modelos import bd, Usuarios
from sqlalchemy.orm import sessionmaker, Session
from pwdlib import PasswordHash
from jose import jwt , JWTError
from main import SECRET_KEY, ALGORITHM, oauth2_schema

password_hash = PasswordHash.recommended()

def pegar_sessao():
    try:
        Session = sessionmaker(bind=bd)
        session = Session()
        yield session
    finally:
        session.close()


def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    #verificaçao de token:
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = int(dic_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="acesso negado, verifique a validade")
    usuario = session.query(Usuarios).filter(Usuarios.id==id_usuario).first() 
    if not usuario:
        raise HTTPException (status_code=401, detail="acesso invalido")
    return usuario