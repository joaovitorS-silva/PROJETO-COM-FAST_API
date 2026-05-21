from fastapi import APIRouter , Depends ,HTTPException
from schemas import PedidoSchema , ItemPedidoSchema
from dependencias import pegar_sessao, verificar_token
from sqlalchemy.orm import Session
from modelos import Pedido , Usuarios, ItemPedido

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"], dependencies=[Depends(verificar_token)])

@order_router.get("/")
async def pedidos():
    """
    essa é rota padrã dos pedidos  do nosso sistema. so usuarios autenticados acessam as rotas dos pedidos.
    """
    return {"mensagem": "vc entrou na lista de pedidos "}

@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao),usuario: Usuarios=Depends(verificar_token)):
    if not usuario.adm:
        raise HTTPException(status_code=402, detail="vc n ao é adm")
    pedido_novo = Pedido(usuario=pedido_schema.id_usuario)
    session.add(pedido_novo)
    session.commit()
    return {"mesangem ": f"pedido criado com sucesso do, ID do {pedido_novo.id}"}

@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int ,session: Session= Depends(pegar_sessao),usuario: Usuarios=Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="pedido nao encontrado")
    if not usuario.adm and usuario.id != pedido.id_usuario:
        raise HTTPException(status_code=401, detail="você não permissão para essa função")
    
    pedido.status = "CANCELADO" 
    session.commit()
    return {
        "mensagem": f"pedido numero{pedido.id} cancelado com sucesso",
       "pedido": pedido
    }
@order_router.get("/lista")
async def listar_pedido( session: Session = Depends(pegar_sessao), usuario: Usuarios = Depends(verificar_token)):
    if not usuario.adm:
        raise HTTPException(status_code=402, detail="apenas adminstradores podem acessar")
    pedido = session.query(Pedido).all()
    return{
        "pedido":pedido
    }

@order_router.post("/adicionar-item{id_pedido}")
async def adicionar_item(id_pedido: int,item_pedido_schema: ItemPedidoSchema, session:Session = Depends(pegar_sessao), usuario: Usuarios= Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail = "pedido nao encontrado")
    if not usuario.adm and usuario.id == pedido.id_usuario:
        raise HTTPException(status_code=401, detail="vc nao tem acesso a este local; ERROR:301")
    item_pedido = ItemPedido(item_pedido_schema.tamanho,item_pedido_schema.quantidade, item_pedido_schema.sabor, item_pedido_schema.preco_unitario, id_pedido)
    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit
    return{
        "mensagem": "item CRIADO COM SUCESSO",
        "item_pedido": item_pedido.id,
        "preco": pedido.preco

    }

@order_router.post("/remover-item{id_item_pedido}")
async def remover_item(id_item_pedido: int, session:Session = Depends(pegar_sessao), usuario: Usuarios= Depends(verificar_token)):
    pedido = session.query(Pedido).filter(ItemPedido.id==id_item_pedido).first()
    item_pedido = session.query(Pedido).filter(Pedido.id == id_item_pedido).first()
    if not item_pedido:
        raise HTTPException(status_code=400, detail = "pedido nao encontrado")
    if not usuario.adm and usuario.id == item_pedido.pedido.id_usuario:
        raise HTTPException(status_code=401, detail="vc nao tem acesso a este local; ERROR:301")
    session.delete(item_pedido)
    item_pedido.pedido.calcular_preco()
    session.commit
    return{
        "mensagem": "item REMOVIDO COM SUCESSO",
        "itens_pedido": pedido.itens,
        "item_pedido": pedido
        }
#finalizar pedido
@order_router.post("/pedido/finalizar/{id_pedido}")
async def finalizar_pedido(id_pedido: int ,session: Session= Depends(pegar_sessao),usuario: Usuarios=Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="pedido nao encontrado")
    if not usuario.adm and usuario.id != pedido.id_usuario:
        raise HTTPException(status_code=401, detail="você não permissão para essa função")
    
    pedido.status = "finalizar" 
    session.commit()
    return {
        "mensagem": f"pedido numero{pedido.id} finalizar com sucesso",
       "pedido": pedido
    }
#visuzalozar 1 pedido 
@order_router.get("/visualizar/{id_pedido}")
async def visulizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao) ,usuario: Usuarios = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=401, detail="pedido nao existe")
    if not usuario.adm and usuario.id != pedido.id_usuario:
        raise HTTPException(status_code=402, detail="vc nao tem premisao para isso")
    return{
        "quantidade_de_itens_no_pedido": len (pedido.itens),
        "pedido": pedido
    }
    #visulizar todos os  pedidos de 1 usuario
@order_router.post("/listar/pedido-usuario")
async def listar_usuario(session: Session = Depends(pegar_sessao), usuario: Usuarios = Depends(verificar_token)):
    pedido_usuario = session.query(Pedido).filter(Pedido.id_usuario==usuario.id).all()
    return{
        "pedido": pedido_usuario
    }
   

