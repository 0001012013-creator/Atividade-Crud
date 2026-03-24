import sqlite3  # Importa a biblioteca SQLite para manipulação do banco de dados

# Cria (ou conecta) ao banco de dados SQLite
conn = sqlite3.connect('estoque_papelaria.db')

# Cria um cursor, que é responsável por executar comandos SQL
cursor = conn.cursor()

# Cria a tabela "produtos" caso ela ainda não exista
cursor.execute('''
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  # Identificador único automático
    nome TEXT NOT NULL,                    # Nome do produto (obrigatório)
    quantidade INTEGER NOT NULL,           # Quantidade em estoque (obrigatório)
    preco REAL NOT NULL                    # Preço do produto (obrigatório)
)
''')

# Salva as alterações no banco de dados
conn.commit()

# Fecha a conexão com o banco (boa prática)
conn.close()

# Mensagem indicando que o banco foi criado com sucesso
print("Banco criado com sucesso!")
