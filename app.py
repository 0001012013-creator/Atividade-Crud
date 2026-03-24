from flask import Flask, jsonify, request  # Importa funções do Flask para criar API e lidar com requisições
import sqlite3  # Biblioteca para trabalhar com banco de dados SQLite

app = Flask(__name__)  

# Função para executar comandos no banco de dados
def executar_query(query, *args, fetch=False, commit=False):
    conn = sqlite3.connect('estoque_papelaria.db')  # Conecta ao banco de dados
    conn.row_factory = sqlite3.Row  # Retorna resultados como dicionário 
    cursor = conn.cursor()  # Cria um cursor para executar comandos SQL
    resultado = None  # Variável para armazenar o retorno da consulta

    try:
        cursor.execute(query, args)  # Executa a query com os parâmetros

        if commit:
            conn.commit()  # Salva alterações no banco (INSERT, UPDATE, DELETE)

        if fetch:
            resultado = cursor.fetchall()  # Busca todos os resultados da consulta

    finally:
        conn.close()  # Fecha a conexão com o banco sempre

    return resultado  # Retorna os dados (se houver)

# Rota para listar todos os produtos OU buscar por ID
@app.route('/produtos', methods=['GET'])
@app.route('/produtos/<int:id>', methods=['GET'])
def gerenciar_produtos(id=None):

    # Se o ID for informado, busca um produto específico
    if id:
        produto = executar_query(
            "SELECT * FROM produtos WHERE id = ?", id, fetch=True
        )

        if produto:
            return jsonify(dict(produto[0])), 200  # Retorna o produto encontrado

        return jsonify({"erro": "Produto não encontrado"}), 404  # Produto não existe

    # Caso não tenha ID, retorna todos os produtos
    dados = executar_query(
        "SELECT id, nome, quantidade, preco FROM produtos", fetch=True
    )

    lista_produtos = [dict(item) for item in dados]  # Converte para lista de dicionários
    return jsonify(lista_produtos), 200

# Rota para criar um novo produto
@app.route('/insert', methods=['POST'])
def criar_produto():
    dados = request.get_json()  # Recebe os dados enviados no corpo da requisição

    executar_query(
        "INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)",
        dados.get('nome'),
        dados.get('quantidade'),
        dados.get('preco'),
        commit=True
    )

    return jsonify({"mensagem": "Produto criado com sucesso!"}), 201  # Status 201 = criado

# Rota para atualizar um produto existente
@app.route('/update/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    dados = request.get_json()  # Recebe os novos dados

    # Verifica se o produto existe
    existe = executar_query(
        "SELECT id FROM produtos WHERE id = ?", id, fetch=True
    )

    if not existe:
        return jsonify({"erro": "Produto não encontrado"}), 404

    # Atualiza o produto no banco
    executar_query(
        "UPDATE produtos SET nome = ?, quantidade = ?, preco = ? WHERE id = ?",
        dados.get('nome'),
        dados.get('quantidade'),
        dados.get('preco'),
        id,
        commit=True
    )

    # Status 204 = sucesso sem conteúdo
    return '', 204

# Rota para deletar um produto
@app.route('/delete/<int:id>', methods=['DELETE'])
def deletar_produto(id):

    # Busca o produto antes de deletar
    produto = executar_query(
        "SELECT nome FROM produtos WHERE id = ?", id, fetch=True
    )

    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404

    # Deleta o produto do banco
    executar_query(
        "DELETE FROM produtos WHERE id = ?", id, commit=True
    )

    return jsonify({"mensagem": f"Produto '{produto[0]['nome']}' removido!"}), 200

# Inicia a aplicação
if __name__ == '__main__':
    app.run(debug=True)
