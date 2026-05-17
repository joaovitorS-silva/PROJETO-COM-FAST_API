from pydantic import BaseModel
from typing import Optional

class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    numero: str
    ativo: Optional[bool]
    adm: Optional[bool]

    class Config:
        from_attributes = True # esse comando faz com que a classe UsuarioSchemas
                                #se tranforme em um objeto, pois de forma padrao 
                                # aquilo ali é um dicionario,E NAO FUNCIONJA  para colcoar no banco de dados
                                #JA O OBJETO FUNCIONA

class PedidoSchema(BaseModel):
    id_usuario: int


    class Config:
        from_attributes = True


class LoginSchemas(BaseModel):
    email: str
    senha:str


    class Config:
        from_attributes = True