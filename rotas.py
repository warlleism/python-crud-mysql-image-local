import base64
from flask import Flask, jsonify, request
from config import conexao, cursor

app = Flask(__name__)

# Rota para buscar livros


@app.route('/buscar_livros', methods=['GET'])
def buscar_livros():
    comando = "SELECT * FROM LIVROS"
    cursor.execute(comando)
    livros = cursor.fetchall()

    livros_json = []
    for livro in livros:
        livro_dict = {
            'id': livro[0],
            'name': livro[1],
            'category': livro[2],
            'price': livro[3],
            'description': livro[4]
        }

        with open(livro[5], "rb") as arquivo_imagem:
            imagem_base64 = base64.b64encode(
                arquivo_imagem.read()).decode('utf-8')

        livro_dict['image'] = imagem_base64

        livros_json.append(livro_dict)

    return jsonify({'livros': livros_json})

# Rota para criação de livro


@app.route('/adicionar_livro', methods=['POST'])
def adicionar_livro():
    dados = request.json

    imagem_base64 = dados['image']
    nome_imagem = dados['name'] + '.jpg'
    caminho_imagem = 'imagens/' + nome_imagem
    with open(caminho_imagem, 'wb') as arquivo:
        arquivo.write(base64.b64decode(imagem_base64))

    comando = "INSERT INTO LIVROS (NAME, CATEGORY, PRICE, DESCRIPTION, IMAGE) VALUES (%s, %s, %s, %s, %s)"
    valores = (dados['name'], dados['category'],
               dados['price'], dados['description'], caminho_imagem)

    cursor.execute(comando, valores)
    conexao.commit()

    return jsonify({'message': 'Livro adicionado com sucesso'})

# Rota para edição de livro


@app.route('/editar_livro', methods=['PUT'])
def editar_livro():
    dados = request.json
    comando = "UPDATE LIVROS SET NAME = %s, CATEGORY = %s, PRICE = %s, DESCRIPTION = %s WHERE ID = %s"
    valores = (dados['name'], dados['category'],
               dados['price'], dados['description'], dados['id'])

    cursor.execute(comando, valores)
    conexao.commit()

    return jsonify({'message': 'Livro editado com sucesso'})

# Rota para deletar livro


@app.route('/deletar_livro', methods=['DELETE'])
def delete_livro():
    dados = request.json
    comando = "DELETE FROM LIVROS WHERE ID = %s"
    valores = (dados['id'],)

    cursor.execute(comando, valores)
    conexao.commit()

    return jsonify({'message': 'Livro deletado com sucesso'})


if __name__ == '__main__':
    app.run(debug=True)
