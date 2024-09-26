from flask import Flask, render_template, redirect, request  # Importa as bibliotecas necessárias do Flask

app = Flask(__name__)  # Cria uma instância da aplicação Flask

@app.route("/", methods=['GET', 'POST'])  # Define a rota para a página inicial, permitindo GET e POST
def index():
    if request.method == 'POST':  # Verifica se o método da requisição é POST
        nome = request.form.get('nome')  # Obtém o nome do formulário
        peso = request.form.get('peso')  # Obtém o peso do formulário
        altura = request.form.get('altura')  # Obtém a altura do formulário

        # Converte peso e altura para float, caso não estejam vazios
        peso = float(peso) if peso else 0  
        altura = float(altura) if altura else 0 
        
        # Calcula o IMC se a altura for maior que 0
        if altura > 0:
            imc = peso / (altura * altura)  # Cálculo do IMC
        else:
            imc = 0  # Se altura for 0 ou inválida, IMC é 0
        
        # Determina o índice de IMC com base no valor calculado
        if imc <= 17:
            indice_imc = "Muito Abaixo do peso"
        elif imc <= 18.49:
            indice_imc = "Abaixo do peso"
        elif imc <= 24.99:
            indice_imc = "Peso Ideal"
        elif imc <= 29.99:
            indice_imc = "Sobrepeso"
        elif imc <= 34.99:
            indice_imc = "Obesidade Grau I"
        elif imc <= 39.99:
            indice_imc = "Obesidade Grau II"
        else:
            indice_imc = "Obesidade Grau III"

        caminho_arquivo = 'models/imc.txt'  # Caminho do arquivo para armazenar os dados

        # Abre o arquivo em modo de adição
        with open(caminho_arquivo, 'a') as arquivo:
            # Escreve os dados no arquivo com formatação adequada
            arquivo.write(f"{nome};{peso};{altura};{imc:.2f};{indice_imc}\n")

        # Renderiza o template 'index.html' passando os dados para o contexto
        return render_template("index.html", peso=peso, altura=altura, 
                               imc=imc, indice_imc=indice_imc)
    else:
        # Se o método não for POST, apenas renderiza o template sem dados
        return render_template("index.html")
    
@app.route("/lista")  # Define a rota para consultar a lista de IMCs
def consultar_imc():
    imc_list = []  # Lista para armazenar os dados de IMC lidos do arquivo
    caminho_arquivo = 'models/imc.txt'  # Caminho do arquivo com os dados de IMC

    # Abre o arquivo em modo de leitura
    with open(caminho_arquivo, 'r') as arquivo:
        # Lê cada linha do arquivo
        for linha in arquivo:
            # Divide a linha em partes usando ';' como delimitador
            item = linha.strip().split(';')
            # Adiciona os dados à lista como um dicionário
            imc_list.append({
                'nome': item[0],  # Nome do usuário
                'peso': item[1],  # Peso do usuário
                'altura': item[2],  # Altura do usuário
                'imc': item[3],  # IMC calculado
                'indice_imc': item[4],  # Índice de IMC
            })

    # Renderiza o template 'imc.html' passando a lista de IMCs
    return render_template("imc.html", imc=imc_list)

if __name__ == "__main__":  # Verifica se o script está sendo executado diretamente
    app.run("127.0.0.1", port=80, debug=True)  # Inicia o servidor Flask em modo debug
