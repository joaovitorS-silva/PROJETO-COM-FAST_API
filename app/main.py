from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer # cria estrutura de token que estamos usando
from dotenv import load_dotenv
import os

load_dotenv()#consigo acessar o aquivo env

SECRET_KEY = os.getenv("SECRET_KEY") #busca a variavel secret_ket no env e tras pra ca
ALGORITHM = os.getenv("ALGORITHM")
ACCES_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCES_TOKEN_EXPIRE_MINUTES"))

app = FastAPI()
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")
#lembrando o APIROUTER serve para essa manipulaoçao essa organizao de arquivops de uma forma melhor
from order_routes import  order_router
from auth_routes import  auth_router
    
app.include_router(order_router)
app.include_router(auth_router)
