from fastapi import FastAPI

app = FastAPI()
#lembrando o APIROUTER serve para essa manipulaoçao essa organizao de arquivops de uma forma melhor
from order_routes import  order_router
from auth_routes import  auth_router

app.include_router(order_router)
app.include_router(auth_router)
