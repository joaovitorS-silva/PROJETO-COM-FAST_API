# PedidosAPI

API REST para gerenciamento de pedidos com autenticação JWT, construída com FastAPI, SQLAlchemy e MySQL.

## Visão geral

Este projeto permite:

- cadastro de usuários
- login com JWT
- geração de access token e refresh token
- criação de pedidos
- adição e remoção de itens do pedido
- controle de acesso por usuário e administrador
- documentação interativa via Swagger

## Tecnologias utilizadas

- Python 3.11+
- FastAPI
- Uvicorn
- SQLAlchemy
- MySQL + PyMySQL
- Pydantic
- python-jose
- pwdlib
- python-dotenv
- Alembic

## Estrutura do projeto

```text
PROJETO-COM-FAST_API/
├── app/
│   ├── __init__.py
│   ├── auth_routes.py
│   ├── dependencias.py
│   ├── modelos.py
│   ├── order_routes.py
│   └── schemas.py
├── migraçoes/
├── versions/
├── main.py
├── .env
├── .env.example
├── .gitignore
├── README.md
├── alembic.ini
├── banco.db
└── requirements.txt
```

> O projeto foi reorganizado em uma pasta `app` para deixar a estrutura mais limpa e mais profissional.

## Requisitos

Antes de começar, tenha instalado:

- Python 3.11 ou superior
- MySQL Server
- Git
- pip

## Configuração do ambiente

### 1. Clone o repositório

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd PROJETO-COM-FAST_API
```

### 2. Crie um ambiente virtual

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

Se o arquivo `requirements.txt` ainda não existir, instale manualmente:

```bash
pip install fastapi uvicorn sqlalchemy pymysql python-jose pwdlib python-dotenv alembic python-multipart argon2-cffi
```

### 4. Configure as variáveis de ambiente

Copie o arquivo de exemplo:

```bash
copy .env.example .env
```

Ou no Linux/macOS:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações reais:

```env
SECRET_KEY=sua_chave_super_secreta
ALGORITHM=HS256
ACCES_TOKEN_EXPIRE_MINUTES=30
```

> Nunca envie o arquivo `.env` para o GitHub. Ele está ignorado no `.gitignore`.

## Banco de dados

O projeto está configurado para usar MySQL com a base `bd_pedidos`.

### Crie o banco no MySQL

```sql
CREATE DATABASE bd_pedidos;
```

No arquivo `app/modelos.py`, a conexão está configurada assim:

```python
bd = create_engine("mysql+pymysql://root:1234@localhost/bd_pedidos")
```

Se o seu usuário, senha e nome do banco forem diferentes, ajuste essa string antes de rodar o projeto.

## Rodando o projeto

Na raiz do projeto, execute:

```bash
uvicorn main:app --reload
```

A aplicação ficará disponível em:

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- Redoc: http://127.0.0.1:8000/redoc

## Endpoints principais

### Autenticação

#### Cadastro de usuário

```http
POST /auth/criar_usuario
```

Body de exemplo:

```json
{
  "nome": "João Silva",
  "email": "joao@email.com",
  "senha": "minhasenha123",
  "numero": "84999999999",
  "ativo": true,
  "adm": false
}
```

#### Login com JSON

```http
POST /auth/login
```

```json
{
  "email": "joao@email.com",
  "senha": "minhasenha123"
}
```

Resposta:

```json
{
  "access_token": "<token>",
  "refresh_token": "<refresh_token>",
  "token_type": "bearer"
}
```

#### Login via formulário OAuth2

```http
POST /auth/login-form
```

Esse endpoint é útil para testar no Swagger.

#### Renovar access token

```http
GET /auth/refresh_token
```

### Pedidos

#### Criar pedido

```http
POST /pedidos/pedido
Authorization: Bearer <access_token>
```

Body:

```json
{
  "id_usuario": 1
}
```

#### Listar pedidos

```http
GET /pedidos/lista
Authorization: Bearer <access_token>
```

#### Adicionar item ao pedido

```http
POST /pedidos/adicionar-item/1
Authorization: Bearer <access_token>
```

Body:

```json
{
  "tamanho": "grande",
  "quantidade": 2,
  "sabor": "frango com catupiry",
  "preco_unitario": 49.9
}
```

#### Remover item do pedido

```http
POST /pedidos/remover-item/1
Authorization: Bearer <access_token>
```

#### Cancelar pedido

```http
POST /pedidos/pedido/cancelar/1
Authorization: Bearer <access_token>
```

#### Visualizar pedido

```http
GET /pedidos/visualizar/1
Authorization: Bearer <access_token>
```

## Autenticação

O projeto utiliza JWT para autenticação.

- Access Token: usado para acessar rotas protegidas
- Refresh Token: usado para renovar o access token

Para testar no Swagger ou em requisições HTTP, envie no header:

```http
Authorization: Bearer <access_token>
```

## Modelos principais

### Usuario

- id
- nome
- email
- senha
- numero
- ativo
- adm

### Pedido

- id
- status
- id_usuario
- preco
- itens

### ItemPedido

- id
- tamanho
- quantidade
- sabor
- preco_unitario
- id_pedido

## Migrações com Alembic

Se quiser usar migrações:

```bash
alembic revision --autogenerate -m "descricao da migracao"
alembic upgrade head
```

Para voltar uma migração:

```bash
alembic downgrade -1
```

## Segurança

Antes de subir para o GitHub:

- nunca envie o arquivo `.env`
- nunca envie credenciais reais
- nunca publique tokens ou chaves secretas
- adicione o `.env` no `.gitignore`

## Observações finais

Este projeto já está em uma estrutura mais organizada para continuar evoluindo, porém ainda depende de alguns ajustes de ambiente local, principalmente na conexão do banco e no preenchimento correto do `.env`.

Se qualquer configuração local for diferente da sua máquina, ajuste os valores antes de iniciar o servidor.

## Autor

João Vitor Da Silva Santos
