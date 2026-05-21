# PedidosAPI

> API RESTful para gerenciamento de pedidos (estilo delivery/pizzaria) com autenticação JWT — construída com **FastAPI** e **SQLAlchemy**.

---

## Índice

- [Sobre](#sobre)
- [Tecnologias](#tecnologias)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Rodando o Projeto](#rodando-o-projeto)
- [Rotas da API](#rotas-da-api)
- [Modelos do Banco de Dados](#modelos-do-banco-de-dados)
- [Autenticação](#autenticação)
- [Migrações com Alembic](#migrações-com-alembic)

---

## Sobre

PedidosAPI é uma API de gerenciamento de pedidos com sistema de autenticação baseado em **JWT (JSON Web Tokens)**. Permite cadastro de usuários, login seguro com tokens de acesso e refresh, criação de pedidos, adição de itens e controle de status — com controle de acesso separado entre usuários comuns e administradores.

---

## Tecnologias

| Tecnologia | Uso |
|---|---|
| [FastAPI](https://fastapi.tiangolo.com/) | Framework principal da API |
| [SQLAlchemy](https://www.sqlalchemy.org/) | ORM para banco de dados |
| [Alembic](https://alembic.sqlalchemy.org/) | Migrações do banco de dados |
| [MySQL + PyMySQL](https://pypi.org/project/PyMySQL/) | Banco de dados |
| [python-jose](https://github.com/mpdavis/python-jose) | Geração e verificação de JWT |
| [pwdlib](https://pypi.org/project/pwdlib/) | Hash seguro de senhas |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Gerenciamento de variáveis de ambiente |
| [Pydantic](https://docs.pydantic.dev/) | Validação e schemas de dados |

---

## Estrutura do Projeto

```
PROJETO-COM-FAST_API/
├── alembic/                  # Migrações do banco de dados
│   ├── versions/             # Arquivos de migração gerados
│   └── env.py                # Configuração do Alembic
├── PROJETO-COM-FAST_API/
│   ├── main.py               # Ponto de entrada e configurações globais
│   ├── modelos.py            # Modelos do banco de dados (ORM)
│   ├── schemas.py            # Schemas Pydantic para validação
│   ├── dependencias.py       # Sessão do banco e verificação de token
│   ├── auth_routes.py        # Rotas de autenticação
│   └── order_routes.py       # Rotas de pedidos
├── alembic.ini               # Configuração do Alembic
├── .env                      # Variáveis de ambiente (não versionar!)
└── .gitignore
```

---

## Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/pedidos-api.git
cd pedidos-api

# Crie e ative um ambiente virtual
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/Mac

# Instale as dependências
pip install fastapi sqlalchemy alembic pymysql python-jose pwdlib python-dotenv uvicorn pydantic
```

---

## Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua_chave_secreta_super_segura
ALGORITHM=HS256
ACCES_TOKEN_EXPIRE_MINUTES=30
```

> **Nunca** versione o `.env` com credenciais reais. Adicione-o ao `.gitignore`.

---

## Rodando o Projeto

```bash
# Aplicar as migrações no banco de dados
alembic upgrade head

# Iniciar o servidor
uvicorn main:app --reload
```

A API estará disponível em `http://127.0.0.1:8000`

Documentação interativa (Swagger UI): `http://127.0.0.1:8000/docs`

---

## Rotas da API

### Autenticação — `/auth`

| Método | Rota | Descrição | Auth? |
|---|---|---|---|
| `GET` | `/auth/` | Rota de status de autenticação | Não |
| `POST` | `/auth/criar_usuario` | Cadastro de novo usuário | Não |
| `POST` | `/auth/login` | Login via JSON (email + senha) | Não |
| `POST` | `/auth/login-form` | Login via formulário OAuth2 (Swagger) | Não |
| `GET` | `/auth/refresh_token` | Gera novo access token com refresh token | Sim |

#### Criar usuário

```json
POST /auth/criar_usuario
{
  "nome": "João Silva",
  "email": "joao@email.com",
  "senha": "minhasenha123",
  "numero": "84999999999",
  "ativo": true,
  "adm": false
}
```

#### Login

```json
POST /auth/login
{
  "email": "joao@email.com",
  "senha": "minhasenha123"
}
```

Resposta:
```json
{
  "access_token": "<jwt_token>",
  "refresh_token": "<jwt_refresh_token>",
  "token_type": "bearer"
}
```

---

### Pedidos — `/pedidos`

> Todas as rotas de pedidos exigem autenticação via Bearer Token.

| Método | Rota | Descrição | Admin? |
|---|---|---|---|
| `GET` | `/pedidos/` | Rota de status dos pedidos | Não |
| `GET` | `/pedidos/lista` | Lista todos os pedidos | Sim |
| `POST` | `/pedidos/pedido` | Cria um novo pedido | Sim |
| `POST` | `/pedidos/pedido/cancelar/{id_pedido}` | Cancela um pedido | Sim ou dono |
| `POST` | `/pedidos/adicionar-item{id_pedido}` | Adiciona item a um pedido | Não |

#### Criar pedido

```json
POST /pedidos/pedido
Authorization: Bearer <access_token>

{
  "id_usuario": 1
}
```

#### Adicionar item ao pedido

```json
POST /pedidos/adicionar-item1
Authorization: Bearer <access_token>

{
  "tamanho": "grande",
  "quantidade": 2,
  "sabor": "frango com catupiry",
  "preco_unitario": 49.90
}
```

---

## Modelos do Banco de Dados

### `Usuarios`

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | Integer | Chave primária |
| `nome` | String | Nome do usuário |
| `email` | String | E-mail (usado no login) |
| `senha` | String | Senha criptografada com hash |
| `numero` | String | Telefone |
| `ativo` | Boolean | Conta ativa (padrão: `True`) |
| `adm` | Boolean | Administrador (padrão: `False`) |

### `Pedido`

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | Integer | Chave primária |
| `status` | String | `PENDENTE`, `CONCLUIDO` ou `CANCELADO` |
| `id_usuario` | FK → `usuarios.id` | Usuário dono do pedido |
| `preco` | Float | Valor total do pedido |

### `ItemPedido`

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | Integer | Chave primária |
| `tamanho` | String | Tamanho do item |
| `quantidade` | Integer | Quantidade |
| `sabor` | String | Sabor do item |
| `preco_unitario` | Float | Preço unitário |
| `pedido` | FK → `pedidos.id` | Pedido associado |

---

## Autenticação

O sistema usa **JWT (JSON Web Tokens)** com dois tipos de token:

- **Access Token** — Válido por `ACCES_TOKEN_EXPIRE_MINUTES` minutos. Usado para acessar rotas protegidas.
- **Refresh Token** — Válido por **7 dias**. Permite renovar o access token sem precisar fazer login novamente.

Para acessar rotas protegidas, envie o token no header:

```
Authorization: Bearer <access_token>
```

O esquema OAuth2 está configurado em `/auth/login-form`, compatível com o botão **Authorize** do Swagger em `/docs`.

---

## Migrações com Alembic

```bash
# Gerar uma nova migração automaticamente
alembic revision --autogenerate -m "descricao da alteracao"

# Aplicar todas as migrações pendentes
alembic upgrade head

# Voltar uma migração
alembic downgrade -1

# Ver o histórico de migrações
alembic history
```

> O arquivo `alembic.ini` deve estar na raiz do projeto e o comando deve ser executado a partir dessa mesma pasta.

---

## Autor
João Vitor da Silva Santos 2º Ano — Informática para Internet - IFRN Campus Caicó
Desenvolvido com FastAPI
