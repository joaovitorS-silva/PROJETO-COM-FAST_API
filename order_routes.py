from fastapi import APIRouter , Depends ,HTTPException
from schemas import PedidoSchema
from dependencias import pegar_sessao, verificar_token
from sqlalchemy.orm import Session
from modelos import Pedido , Usuarios

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"], dependencies=[Depends(verificar_token)])

@order_router.get("/")
async def pedidos():
    """
    essa é rota padrã dos pedidos  do nosso sistema. so usuarios autenticados acessam as rotas dos pedidos.
    """
    return {"mensagem": "vc entrou na lista de pedidos "}

@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    pedido_novo = Pedido(usuario=pedido_schema.id_usuario)
    session.add(pedido_novo)
    session.commit()
    return {"mesangem ": f"pedido criado com sucesso do {pedido_novo.id}"}

@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int ,session: Session= Depends(pegar_sessao),usuario: Usuarios=Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="pedido nao encontrado")
    if not usuario.adm or usuario.id != pedido.id_usuario:
        raise HTTPException(status_code=402, detail="vc nao pode cancelar o pedido")
    session.commit()
    pedido.status = "CANCELADO"
    session.commit()
    return {
        "mensagem": f"pedido numero{id_pedido} cancelado com sucesso",
        "pedido": pedido
    }
