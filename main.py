import os
from datetime import datetime

# Lista de produtos
produtos = []

# Mínimo de estoque para alimentos e acessórios
MIN_ESTOQUE_ALIMENTO = 5
MIN_ESTOQUE_ACESSORIOS = 3

# Função para limpar a tela
def limparTela():
    os.system("cls" if os.name == "nt" else "clear")

# Função para autenticar o usuário
def autenticarUsuario():
    tentativas = 0
    maxTentativas = 3

    while tentativas < maxTentativas:
        usuario = input("Digite o usuário: ")
        senha = input("Digite a senha: ")

        # Verifique o banco de dados de usuários
        if verificarUsuario(usuario, senha):
            return True
        else:
            tentativas += 1
            print(f"Usuário ou senha incorretos! Tentativa {tentativas} de {maxTentativas}")

    print("Número máximo de tentativas atingido!")
    return False

# Função para verificar se o usuário existe no banco de dados
def verificarUsuario(usuario, senha):
    with open("usuarios.txt", "r") as arquivo:
        for linha in arquivo:
            nome, senha_armazenada = linha.strip().split(',')
            if usuario == nome and senha == senha_armazenada:
                return True
    return False

# Criar o arquivo de banco de dados de usuários se ainda não existir
def criarBancoUsuarios():
    usuarios = [
        ("usuario1", "senha1"),
        ("usuario2", "senha2"),
        ("usuario3", "senha3"),
        ("usuario4", "senha4")
    ]

    with open("usuarios.txt", "w") as arquivo:
        for usuario, senha in usuarios:
            arquivo.write(f"{usuario},{senha}\n")

# Verifique se o arquivo de banco de dados de usuários existe
try:
    with open("usuarios.txt", "r"):
        pass
except FileNotFoundError:
    criarBancoUsuarios()

# Função para selecionar a categoria do produto
def selecionarCategoria():
    limparTela()
    print("Selecione uma categoria:")
    print("1. Alimento")
    print("2. Acessorios")
    opcaoCategoria = int(input())

    if opcaoCategoria == 1:
        return "Alimento"
    elif opcaoCategoria == 2:
        return "Acessorios"
    else:
        print("Opção inválida!")
        return None

# Função para registrar um produto
def registrarProduto():
    limparTela()
    print("Digite as informações do produto:")
    produto = {}
    produto["nome"] = input("Nome: ")

    print("Escolha a categoria do produto:")
    produto["categoria"] = selecionarCategoria()

    if not produto["categoria"]:
        return

    produto["quantidade"] = int(input("Quantidade: "))

    produtoExistente = None
    for p in produtos:
        if p["nome"] == produto["nome"] and p["categoria"] == produto["categoria"]:
            produtoExistente = p
            break

    if produtoExistente:
        produtoExistente["quantidade"] += produto["quantidade"]
    else:
        produtos.append(produto)

# Função para listar produtos por categoria
def listarProdutosPorCategoria(categoria):
    limparTela()
    print(f"Produtos disponíveis em {categoria}:")
    indexList = {}
    counter = 1
    for index, produto in enumerate(produtos):
        if produto["categoria"] == categoria and produto["quantidade"] > 0:
            print(f"{counter}. {produto['nome']} - {produto['quantidade']} unidades")
            indexList[counter] = index
            counter += 1
    return indexList

# Função para verificar o estoque de uma categoria
def verificarEstoqueCategoria(categoria):
    for produto in produtos:
        if produto["categoria"] == categoria and produto["quantidade"] > 0:
            return True
    return False

# Função para comprar um produto
def comprarProduto():
    limparTela()
    categoria = selecionarCategoria()
    if not categoria:
        return

    if not verificarEstoqueCategoria(categoria):
        print(f"Não há produtos em estoque na categoria {categoria}!")
        return

    indexList = listarProdutosPorCategoria(categoria)
    escolha = int(input("Selecione o produto pelo número: "))

    if escolha not in indexList:
        print("Seleção inválida!")
        return

    produto = produtos[indexList[escolha]]
    quantidadeCompra = int(input("Quantidade a comprar: "))

    if quantidadeCompra > produto["quantidade"]:
        print("Quantidade insuficiente em estoque!")
        return

    produto["quantidade"] -= quantidadeCompra
    print("Compra efetuada!")

# Função para verificar o estoque
def verEstoque():
    limparTela()
    totalEstoque = 0
    categoriaQuantidade = {}

    for produto in produtos:
        totalEstoque += produto["quantidade"]

        if produto["categoria"] not in categoriaQuantidade:
            categoriaQuantidade[produto["categoria"]] = 0

        categoriaQuantidade[produto["categoria"]] += produto["quantidade"]

    if totalEstoque == 0:
        print("Está sem estoque!")
        return

    for categoria, quantidade in categoriaQuantidade.items():
        porcentagem = (quantidade / totalEstoque) * 100
        print(f"A categoria {categoria} representa {porcentagem:.2f}% do estoque total, com {quantidade} produtos.")

        if categoria == "Alimento" and quantidade < MIN_ESTOQUE_ALIMENTO:
            print("Atenção: Estoque de Alimento está abaixo do mínimo!")
        elif categoria == "Acessorios" and quantidade < MIN_ESTOQUE_ACESSORIOS:
            print("Atenção: Estoque de Acessorios está abaixo do mínimo!")

        if categoria == "Alimento" and quantidade >= MIN_ESTOQUE_ALIMENTO:
            print("Não há necessidade de realizar um novo pedido na categoria " + categoria)
        elif categoria == "Acessorios" and quantidade >= MIN_ESTOQUE_ACESSORIOS:
            print("Não há necessidade de realizar um novo pedido na categoria " + categoria)

# Função para editar um produto
def editarProduto():
    limparTela()
    print("Digite o nome do produto que deseja editar:")
    nome_produto = input("Nome do produto: ")

    for produto in produtos:
        if produto["nome"] == nome_produto:
            print(f"Produto encontrado. Categoria: {produto['categoria']}, Quantidade: {produto['quantidade']}")
            nova_quantidade = int(input("Digite a nova quantidade: "))
            produto["quantidade"] = nova_quantidade
            print("Produto editado com sucesso!")
            return

    print("Produto não encontrado!")

# Função para deletar um produto
def deletarProduto():
    limparTela()
    print("Digite o nome do produto que deseja excluir:")
    nome_produto = input("Nome do produto: ")

    for produto in produtos:
        if produto["nome"] == nome_produto:
            produtos.remove(produto)
            print("Produto excluído com sucesso!")
            return

    print("Produto não encontrado!")

# Função para exportar o relatório de estoque
def exportarRelatorioEstoque():
    limparTela()
    print("Selecione o formato de exportação:")
    print("1. Exportar para .txt")
    print("2. Exportar para .csv")

    opcaoExportacao = int(input())

    if opcaoExportacao == 1:
        exportarParaTxt()
    elif opcaoExportacao == 2:
        exportarParaCsv()
    else:
        print("Opção de formato inválida!")

# Função para exportar o relatório em formato .txt
def exportarParaTxt():
    with open("relatorio_estoque.txt", "w") as arquivo:
        for produto in produtos:
            arquivo.write(f"Nome: {produto['nome']}, Categoria: {produto['categoria']}, Quantidade: {produto['quantidade']}\n")

    print("Relatório de estoque exportado para relatorio_estoque.txt!")

# Função para exportar o relatório em formato .csv
def exportarParaCsv():
    import csv
    with open("relatorio_estoque.csv", mode="w", newline="") as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow(["Nome", "Categoria", "Quantidade"])
        for produto in produtos:
            writer.writerow([produto['nome'], produto['categoria'], produto['quantidade']])

    print("Relatório de estoque exportado para relatorio_estoque.csv!")

# Chame a função autenticarUsuario() para iniciar o sistema
if autenticarUsuario():
    while True:
        limparTela()

        print("Selecione uma opção:")
        print("1. Comprar")
        print("2. Registrar produto")
        print("3. Ver estoque")
        print("4. Editar produto")
        print("5. Deletar produto")
        print("6. Exportar relatório de estoque")
        print("7. Sair")

        opcao = int(input())

        if opcao == 1:
            comprarProduto()
        elif opcao == 2:
            registrarProduto()
        elif opcao == 3:
            verEstoque()
        elif opcao == 4:
            editarProduto()
        elif opcao == 5:
            deletarProduto()
        elif opcao == 6:
            exportarRelatorioEstoque()
        elif opcao == 7:
            limparTela()
            break
        else:
            print("Opção inválida!")

        input("Pressione ENTER para continuar...")
