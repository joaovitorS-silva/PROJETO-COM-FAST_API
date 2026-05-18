# PedidosAPI

> API RESTful para gerenciamento de pedidos com autenticação JWT — construída com **FastAPI** e **SQLAlchemy**.

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

---

## Sobre

PedidosAPI é uma API de gerenciamento de pedidos (estilo delivery/pizzaria) com sistema de autenticação baseado em **JWT (JSON Web Tokens)**. Suporta cadastro de usuários, login seguro com tokens de acesso e refresh, e criação de pedidos com itens associados.

---

## Tecnologias

| Tecnologia | Uso |
|---|---|
| [FastAPI](https://fastapi.tiangolo.com/) | Framework principal da API |
| [SQLAlchemy](https://www.sqlalchemy.org/) | ORM para banco de dados |
| [SQLite](https://www.sqlite.org/) | Banco de dados local |
| [python-jose](https://github.com/mpdavis/python-jose) | Geração e verificação de JWT |
| [pwdlib](https://pypi.org/project/pwdlib/) | Hash seguro de senhas |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Gerenciamento de variáveis de ambiente |
| [Pydantic](https://docs.pydantic.dev/) | Validação e schemas de dados |

---

## Estrutura do Projeto

```
projeto/
├── main.py           # Ponto de entrada da aplicação e configurações globais
├── modelos.py        # Modelos do banco de dados (ORM)
├── schemas.py        # Schemas Pydantic para validação de dados
├── dependencias.py   # Sessão do banco e verificação de token
├── auth_routes.py    # Rotas de autenticação (registro, login, token)
├── order_routes.py   # Rotas de pedidos
└── .env              # Variáveis de ambiente (não versionar!)
```

---

## Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/pedidos-api.git
cd pedidos-api

# Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instale as dependências
pip install fastapi sqlalchemy python-jose pwdlib python-dotenv uvicorn pydantic
```

---

## Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
SECRET_KEY=sua_chave_secreta_super_segura
ALGORITHM=HS256
ACCES_TOKEN_EXPIRE_MINUTES=30
```

> **Nunca** versione o `.env` com credenciais reais. Adicione-o ao `.gitignore`.

---

## Rodando o Projeto

```bash
uvicorn main:app --reload
```

A API estará disponível em `http://127.0.0.1:8000`.

Documentação interativa (Swagger UI): `http://127.0.0.1:8000/docs`

---

## Rotas da API

### Autenticação — `/auth`

| Método | Rota | Descrição | Auth? |
|---|---|---|---|
| `GET` | `/auth/` | Rota de status de autenticação | Não |
| `POST` | `/auth/criar_usuario` | Cadastro de novo usuário | Não |
| `POST` | `/auth/login` | Login via JSON (email + senha) | Não |
| `POST` | `/auth/login-form` | Login via formulário OAuth2 | Não |
| `GET` | `/auth/refresh_token` | Gera novo access token com refresh token | Sim |

#### Exemplo — Criar usuário

```json
POST /auth/criar_usuario
{
  "nome": "João Silva",
  "email": "joao@email.com",
  "senha": "minhasenha123",
  "numero": "84999999999"
}
```

#### Exemplo — Login

```json
POST /auth/login
{
  "email": "joao@email.com",
  "senha": "minhasenha123"
}
```

**Resposta:**
```json
{
  "access_token": "<jwt_token>",
  "refresh_token": "<jwt_refresh_token>",
  "token_type": "bearer"
}
```

---

### Pedidos — `/pedidos`

| Método | Rota | Descrição | Auth? |
|---|---|---|---|
| `GET` | `/pedidos/` | Lista de pedidos | Não |
| `POST` | `/pedidos/pedido` | Cria um novo pedido | Não |

#### Exemplo — Criar pedido

```json
POST /pedidos/pedido
{
  "id_usuario": 1
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
| `status` | String | Status: `PENDENTE`, `CONCLUIDO`, `CANCELADO` |
| `id_usuario` | FK → `usuarios.id` | Usuário dono do pedido |
| `preco` | Float | Valor total do pedido |

### `itenspedido`

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | Integer | Chave primária |
| `tamanho` | String | Tamanho do item |
| `sabor` | String | Sabor do item |
| `preco_unitario` | Float | Preço unitário |
| `pedido` | FK → `pedidos.id` | Pedido associado |

---

## Autenticação

O sistema usa **JWT (JSON Web Tokens)** com dois tipos de token:

- **Access Token** — Válido por `ACCES_TOKEN_EXPIRE_MINUTES` minutos. Usado para acessar rotas protegidas.
- **Refresh Token** — Válido por **7 dias**. Usado para renovar o access token sem precisar logar novamente.

Para acessar rotas protegidas, envie o token no header:

```
Authorization: Bearer <access_token>
```

O esquema OAuth2 está configurado em `/auth/login-form`, compatível com a documentação Swagger em `/docs`.

---

## Autor

Desenvolvido com FastAPI.
