from fastapi import APIRouter

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@order_router.get("/")
async def pedidos():
    """
    essa é rota padrã dos pedidos  do nosso sistema. so usuarios autenticados acessam as rotas dos pedidos.
    """
    return {"mensagem": "vc entrou na lista de pedidos "}