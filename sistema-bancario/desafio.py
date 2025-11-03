# variáveis
saldo = 0
limite = 500
extrato = ""
numero_saques = 0
lista_usuarios = []
lista_contas = []

# constantes
LIMITE_SAQUES = 3
AGENCIA = "0001"

def menu():
    menu = """\n
    ======== MENU ========
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nu] Novo Usuário
    [lu] Listar Usuários
    [nc] Nova Conta
    [lc] Listar Contas
    [q] Sair
    => """
    return input(menu)

# positional only
def deposito(saldo, valor, extrato):
    if valor  > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
    else:
        print("Operação falhou! Valor inválido!")
    
    return saldo, extrato

# keyword only
def saque(*,saldo, valor, extrato, limite, numero_saques, limite_saques):
    if saldo >= valor and valor <= limite and numero_saques <= limite_saques:
        saldo -= valor
        numero_saques += 1
        extrato += f"Saque: R$ {valor:.2f}\n"
    elif saldo < valor:
        print("Operação falhou! Saldo insuficiente.")
    elif valor > limite:
        print("Operação falhou! Valor do saque excede o limite.")
    elif numero_saques >= limite_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    else:
        print("Operação falhou! Verifique os dados informados.")
    
    return saldo, extrato, numero_saques

# positional only e keyword only
def mostra_extrato(saldo,*,extrato):
    print("\n================ EXTRATO ================")
    if extrato != "":
        print(extrato)
    else:
        print("Não foram realizadas movimentações.")
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")
    return

# novas funcoes criar usuario e criar conta
# endereco = logradouro, nro - bairro - cidade/sigla estado
# deve ser armazenado somente numeros do cpf
# nao podem ser cadastrados 2 usuarios com o mesmo cpf
def criar_usuario(nome, data_nascimento, cpf, endereco, lista_usuarios):
    for usuario in lista_usuarios:
        if usuario["cpf"] == cpf:
            print("Erro! Já existe um usuário cadastrado com esse CPF!")
            return lista_usuarios
    usuario = {"nome":nome,"data_nascimento":data_nascimento,"cpf":cpf,"endereco":endereco}
    lista_usuarios.append(usuario)
    return lista_usuarios

def filtrar_usuario(cpf, lista_usuarios):
    usuarios_filtrados = [usuario for usuario in lista_usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

# o numero da agencia é fixo "0001"
# um usuario pode ter mais de uma conta
# uma conta pertence somente a um usuario
# para vincular, buscar o usuario pelo cpf filtrando a lista de usuarios
def criar_conta(agencia, numero_conta, usuario, lista_contas):
    if filtrar_usuario(usuario["cpf"], lista_usuarios):
        conta = {"agencia":agencia, "numero_conta":numero_conta, "usuario":usuario}
        lista_contas.append(conta)
        return lista_contas
    else:
        print("Erro! Usuário não encontrado.")
        return lista_contas

# funcao extra: listar contas
def mostra_contas(listas_contas):
    for conta in lista_contas:
        print(lista_contas)
    return

# funcao extra: listar usuarios
def mostra_usuarios(lista_usuarios):
    for usuario in lista_usuarios:
        print(lista_usuarios)
    return

# funçao principal
def main():
    while True:

        opcao = menu()

        if opcao == "d":
            valor = float(input("\nInforme o valor do depósito: "))
            saldo, extrato = deposito(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("\nInforme o valor do saque: "))
            saldo, extrato, numero_saques = saque(saldo=saldo, valor=valor, extrato=extrato, limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES)

        elif opcao == "e":
            mostra_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            nome = input("Informe o nome completo: ")
            data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
            cpf = input("Informe o CPF (somente números): ")
            endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
            lista_usuarios = criar_usuario(nome, data_nascimento, cpf, endereco, lista_usuarios)

        elif opcao == "lu":
            mostra_usuarios(lista_usuarios)

        elif opcao == "nc":
            cpf = input("Informe o CPF do usuário: ")
            usuario = filtrar_usuario(cpf, lista_usuarios)
            if usuario:
                numero_conta = len(lista_contas) + 1
                lista_contas = criar_conta(AGENCIA, numero_conta, usuario, lista_contas)
                print("Conta criada com sucesso!")
            else:
                print("Erro! Usuário não encontrado!")

        elif opcao == "lc":
            mostra_contas(lista_contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")



main()