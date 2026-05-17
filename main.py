from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()#consigo acessar o aquivo env

SECRET_KEY = os.getenv("SECRET_KEY") #busca a variavel secret_ket no env e tras pra ca


app = FastAPI()

#lembrando o APIROUTER serve para essa manipulaoçao essa organizao de arquivops de uma forma melhor
from order_routes import  order_router
from auth_routes import  auth_router
    
app.include_router(order_router)
app.include_router(auth_router)
