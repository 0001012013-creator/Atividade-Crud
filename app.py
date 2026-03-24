from flask import Flask, jsonify, request # Realiza as importações necessarias 
import sqlite3

app = Flask(__name__)  

def executar_query(query, *args, fetch=False, commit=False): # Função para executar as querys no banco de dados
    conn = sqlite3.connect('estoque_papelaria.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    resultado = None
    
    try:
        cursor.execute(query, args)
        
        if commit:
            conn.commit()
        if fetch:
            resultado = cursor.fetchall()
    finally:
        conn.close()
    
    return resultado

@app.route('/produtos', methods=['GET']) 
@app.route('/produtos/<int:id>', methods=['GET'])
def gerenciar_produtos(id=None):
    if id:
        produto = executar_query("SELECT * FROM produtos WHERE id = ?", id, fetch=True)
        if produto:
            return jsonify(dict(produto[0])), 200
        return jsonify({"erro": "Produto não encontrado"}), 404

    dados = executar_query("SELECT id, nome, quantidade, preco FROM produtos", fetch=True)
    lista_produtos = [dict(item) for item in dados]
    return jsonify(lista_produtos), 200

@app.route('/insert', methods=['POST'])
def criar_produto():
    dados = request.get_json()
    executar_query(
        "INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)",
        dados.get('nome'), dados.get('quantidade'), dados.get('preco'),
        commit=True
    )
    return jsonify({"mensagem": "Produto criado com sucesso!"}), 201

@app.route('/update/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    dados = request.get_json()
    
    existe = executar_query("SELECT id FROM produtos WHERE id = ?", id, fetch=True)
    if not existe:
        return jsonify({"erro": "Produto não encontrado"}), 404

    executar_query(
        "UPDATE produtos SET nome = ?, quantidade = ?, preco = ? WHERE id = ?",
        dados.get('nome'), dados.get('quantidade'), dados.get('preco'), id,
        commit=True
    )
    return jsonify({"mensagem": "Produto atualizado com sucesso!"}), 204

@app.route('/delete/<int:id>', methods=['DELETE'])
def deletar_produto(id):
    produto = executar_query("SELECT nome FROM produtos WHERE id = ?", id, fetch=True)
    
    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404

    executar_query("DELETE FROM produtos WHERE id = ?", id, commit=True)
    return jsonify({"mensagem": f"Produto '{produto[0]['nome']}' removido!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
