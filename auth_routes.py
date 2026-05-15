from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["autenticaçao"])

@auth_router.get("/")
async def autenticador():
    """
    essa é rota padrão de autenticação  do nosso sistema
    """
    return{"mensagem": "vc estar autenticado", "autenticado": False}

