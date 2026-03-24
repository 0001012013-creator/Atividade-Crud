# API de Estoque de jogos

Projeto de API REST desenvolvida com **Python + Flask + SQLite** para gerenciamento de produtos de papelaria.

---

## Tecnologias utilizadas

* Python
* Flask
* SQLite
* API REST
* JSON

---

## Estrutura do projeto

```
CRUD/
│
├── app.py              # API principal
├── estoque_papelaria.db
├── init_db.py          # Script para criar o banco
├── README.md
└── requirements.txt
```

---

## Instalação e execução 
### 1. Criar ambiente virtual

```bash
python -m venv venv
```

---

### 2. Ativar o ambiente

**Windows:**

```bash
venv\Scripts\activate
```

### 3. Instalar dependências (Flask)

```bash
python -m pip install flask
```

---

### 4. Criar o banco de dados

```bash
python init_db.py
```

---

### 5. Executar a API

```bash
python app.py
```

A API estará disponível em:

```
http://127.0.0.1:5000
```

---

## Testes da API (com curl)
### Criar produto (POST)

```bash
curl -X POST http://127.0.0.1:5000/insert ^
-H "Content-Type: application/json" ^
-d "{\"nome\":\"God of war\",\"quantidade\":3,\"preco\":21.50}"
```

---

### Listar todos os produtos (GET)

```bash
curl http://127.0.0.1:5000/produtos
```

---

### Buscar produto por ID (GET)

```bash
curl http://127.0.0.1:5000/produtos/1
```

---

### Atualizar produto (PUT)

```bash
curl -X PUT http://127.0.0.1:5000/update/1 ^
-H "Content-Type: application/json" ^
-d "{\"nome\":\"God of war\",\"quantidade\":20,\"preco\":15.90}"
```

---

### Deletar produto (DELETE)

```bash
curl -X DELETE http://127.0.0.1:5000/delete/1
```

---

## Descrição das rotas

GET     ==> /produtos       ==> Lista todos os produtos       
GET     ==> /produtos/<id>  ==> Busca produto por ID          
POST    ==> /insert         ==> Cria um novo produto          
PUT     ==> /update/<id>    ==> Atualiza um produto existente 
DELETE  ==> /delete/<id>    ==> Remove um produto             

---

## Funcionalidades

* CRUD completo
* Retorno em JSON
* Validação básica de dados

---

## Observações importantes

* Todos os produtos devem conter:

  * `nome`
  * `quantidade`
  * `preco`

* O campo `id` é gerado automaticamente pelo banco.
* Caso algum dado obrigatório não seja enviado, pode ocorrer erro no banco.
