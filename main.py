produtos = []

MIN_ESTOQUE_ALIMENTO = 5
MIN_ESTOQUE_ACESSORIOS = 3

def limparTela():
    import os
    os.system("cls")

def autenticarUsuario():
    tentativas = 0
    maxTentativas = 3
    while tentativas < maxTentativas:
        usuario = input("Digite o usuário: ")
        senha = input("Digite a senha: ")

        if usuario == "admin" and senha == "@dmiN":
            return True
        else:
            tentativas += 1
            print(f"Usuário ou senha incorretos! Tentativa {tentativas} de {maxTentativas}")
    return False

def selecionarCategoria():
    limparTela()
    print("Selecione uma categoria:")
    print("1. Alimento")
    print("2. Acessórios")
    opcaoCategoria = int(input())

    if opcaoCategoria == 1:
        return "Alimento"
    elif opcaoCategoria == 2:
        return "Acessórios"
    else:
        print("Opção inválida!")
        return None

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

def verificarEstoqueCategoria(categoria):
    limparTela()
    for produto in produtos:
        if produto["categoria"] == categoria and produto["quantidade"] > 0:
            return True
    return False

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
        elif categoria == "Acessórios" and quantidade < MIN_ESTOQUE_ACESSORIOS:
            print("Atenção: Estoque de Acessórios está abaixo do mínimo!")

        if categoria == "Alimento" and quantidade >= MIN_ESTOQUE_ALIMENTO:
            print("Não há necessidade de realizar um novo pedido na categoria " + categoria)
        elif categoria == "Acessórios" and quantidade >= MIN_ESTOQUE_ACESSORIOS:
            print("Não há necessidade de realizar um novo pedido na categoria " + categoria)

if not autenticarUsuario():
    print("Número máximo de tentativas atingido!")
else:
    while True:
        limparTela()

        print("Selecione uma opção:")
        print("1. Comprar")
        print("2. Registrar produto")
        print("3. Ver estoque")
        print("4. Sair")

        opcao = int(input())

        if opcao == 1:
            comprarProduto()
        elif opcao == 2:
            registrarProduto()
        elif opcao == 3:
            verEstoque()
        elif opcao == 4:
            limparTela()
            break
        else:
            print("Opção inválida!")

        input("Pressione ENTER para continuar...")
