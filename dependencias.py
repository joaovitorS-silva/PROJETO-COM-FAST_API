from modelos import bd
from sqlalchemy.orm import sessionmaker
from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()

def pegar_sessao():
    try:
        Session = sessionmaker(bind=bd)
        session = Session()
        yield session
    finally:
        session.close()