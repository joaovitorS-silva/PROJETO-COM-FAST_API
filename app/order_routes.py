from fastapi import APIRouter , Depends
from schemas import PedidoSchema
from dependencias import pegar_sessao
from sqlalchemy.orm import Session
from modelos import Pedido

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"])

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
    return {"mesangem  " f"pedido criado com sucesso do if {pedido_novo.id}"}